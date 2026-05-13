import sqlite3
import pandas as pd
import os

db_path = os.path.join('data', 'processed', 'health_analytics.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Loading data...")

# ── LOAD CSV (one file has everything) ─────────────────────
df = pd.read_csv('data/raw/covid-deaths.csv', encoding='utf-8-sig')
print(f"Total rows loaded: {len(df)}")

# ── CLEAN: drop continent/world aggregate rows ─────────────
df = df[df['code'].notna()]
df = df[~df['code'].str.startswith('OWID')]
print(f"Rows after removing aggregates: {len(df)}")

# ── DIM: COUNTRIES ─────────────────────────────────────────
print("\nLoading dim_countries...")
countries = df[['country', 'code', 'continent', 'population']].drop_duplicates('code')

for _, row in countries.iterrows():
    cursor.execute('''
        INSERT OR IGNORE INTO dim_countries (country_name, iso_code, region, population, income_level)
        VALUES (?, ?, ?, ?, ?)
    ''', (row['country'], row['code'], row['continent'], row['population'], None))

conn.commit()
print(f"✅ {len(countries)} countries loaded")

# ── DIM: DISEASES ──────────────────────────────────────────
print("\nLoading dim_diseases...")
cursor.execute('''
    INSERT OR IGNORE INTO dim_diseases (disease_name, disease_category, is_communicable)
    VALUES ('COVID-19', 'Infectious', 1)
''')
conn.commit()
cursor.execute("SELECT disease_key FROM dim_diseases WHERE disease_name = 'COVID-19'")
covid_key = cursor.fetchone()[0]
print(f"✅ COVID-19 loaded (disease_key={covid_key})")

# ── DIM: DATES ─────────────────────────────────────────────
print("\nLoading dim_dates...")
df['date'] = pd.to_datetime(df['date'])
all_dates = df['date'].dropna().unique()

for d in all_dates:
    d = pd.Timestamp(d)
    date_key = int(d.strftime('%Y%m%d'))
    cursor.execute('''
        INSERT OR IGNORE INTO dim_dates (date_key, full_date, year, month, day, quarter)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (date_key, str(d.date()), d.year, d.month, d.day, (d.month - 1) // 3 + 1))

conn.commit()
print(f"✅ {len(all_dates)} dates loaded")

# ── BUILD COUNTRY LOOKUP ───────────────────────────────────
cursor.execute("SELECT country_name, country_key FROM dim_countries")
country_map = dict(cursor.fetchall())

# ── FACT: DISEASE CASES ────────────────────────────────────
print("\nLoading fact_disease_cases...")
batch_cases = []
for _, row in df.iterrows():
    c_key    = country_map.get(row['country'])
    date_key = int(row['date'].strftime('%Y%m%d'))
    cases    = row.get('new_cases')
    deaths   = row.get('new_deaths')
    cfr      = round(float(deaths) / float(cases) * 100, 2) if pd.notna(cases) and pd.notna(deaths) and float(cases) > 0 else None

    if c_key:
        batch_cases.append((c_key, covid_key, date_key, cases, deaths, cfr, 'Our World in Data'))

cursor.executemany('''
    INSERT INTO fact_disease_cases
        (country_key, disease_key, date_key, cases_count, deaths_count, case_fatality_rate, data_source)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', batch_cases)
conn.commit()
print(f"✅ {len(batch_cases)} case records loaded")

# ── FACT: VACCINATIONS ─────────────────────────────────────
print("\nLoading fact_vaccination_rates...")
batch_vax = []
for _, row in df.iterrows():
    c_key    = country_map.get(row['country'])
    date_key = int(row['date'].strftime('%Y%m%d'))
    pv       = row.get('people_vaccinated')
    fv       = row.get('people_fully_vaccinated')
    rate     = row.get('people_vaccinated_per_hundred')

    if c_key and (pd.notna(pv) or pd.notna(fv) or pd.notna(rate)):
        batch_vax.append((c_key, covid_key, date_key, pv, fv, rate, 'Our World in Data'))

cursor.executemany('''
    INSERT INTO fact_vaccination_rates
        (country_key, disease_key, date_key, people_vaccinated, fully_vaccinated, vaccination_rate, data_source)
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', batch_vax)
conn.commit()
print(f"✅ {len(batch_vax)} vaccination records loaded")

# ── FACT: MORTALITY ────────────────────────────────────────
print("\nLoading fact_mortality...")
batch_mort = []
for _, row in df.iterrows():
    c_key    = country_map.get(row['country'])
    date_key = int(row['date'].strftime('%Y%m%d'))
    deaths   = row.get('new_deaths')
    rate     = row.get('total_deaths_per_million')

    if c_key and pd.notna(deaths):
        batch_mort.append((c_key, covid_key, date_key, deaths, rate, 'Our World in Data'))

cursor.executemany('''
    INSERT INTO fact_mortality
        (country_key, disease_key, date_key, deaths_count, mortality_rate, data_source)
    VALUES (?, ?, ?, ?, ?, ?)
''', batch_mort)
conn.commit()
print(f"✅ {len(batch_mort)} mortality records loaded")

conn.close()
print("\n🎉 All data loaded successfully!")