import sqlite3
import os

# Create database in data/processed folder
db_path = os.path.join('data', 'processed', 'health_analytics.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Creating database tables...")

# ── DIMENSION TABLES ──────────────────────────────────────

cursor.execute('''
CREATE TABLE IF NOT EXISTS dim_countries (
    country_key   INTEGER PRIMARY KEY AUTOINCREMENT,
    country_name  TEXT UNIQUE,
    iso_code      TEXT,
    region        TEXT,
    income_level  TEXT,
    population    INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS dim_dates (
    date_key    INTEGER PRIMARY KEY,
    full_date   TEXT UNIQUE,
    year        INTEGER,
    month       INTEGER,
    day         INTEGER,
    quarter     INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS dim_diseases (
    disease_key      INTEGER PRIMARY KEY AUTOINCREMENT,
    disease_name     TEXT UNIQUE,
    disease_category TEXT,
    is_communicable  INTEGER
)
''')

# ── FACT TABLES ───────────────────────────────────────────

cursor.execute('''
CREATE TABLE IF NOT EXISTS fact_disease_cases (
    case_key           INTEGER PRIMARY KEY AUTOINCREMENT,
    country_key        INTEGER,
    disease_key        INTEGER,
    date_key           INTEGER,
    cases_count        REAL,
    deaths_count       REAL,
    case_fatality_rate REAL,
    data_source        TEXT,
    FOREIGN KEY (country_key)  REFERENCES dim_countries(country_key),
    FOREIGN KEY (disease_key)  REFERENCES dim_diseases(disease_key),
    FOREIGN KEY (date_key)     REFERENCES dim_dates(date_key)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS fact_vaccination_rates (
    vaccination_key    INTEGER PRIMARY KEY AUTOINCREMENT,
    country_key        INTEGER,
    disease_key        INTEGER,
    date_key           INTEGER,
    people_vaccinated  REAL,
    fully_vaccinated   REAL,
    vaccination_rate   REAL,
    data_source        TEXT,
    FOREIGN KEY (country_key)  REFERENCES dim_countries(country_key),
    FOREIGN KEY (disease_key)  REFERENCES dim_diseases(disease_key),
    FOREIGN KEY (date_key)     REFERENCES dim_dates(date_key)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS fact_mortality (
    mortality_key  INTEGER PRIMARY KEY AUTOINCREMENT,
    country_key    INTEGER,
    disease_key    INTEGER,
    date_key       INTEGER,
    deaths_count   REAL,
    mortality_rate REAL,
    data_source    TEXT,
    FOREIGN KEY (country_key)  REFERENCES dim_countries(country_key),
    FOREIGN KEY (disease_key)  REFERENCES dim_diseases(disease_key),
    FOREIGN KEY (date_key)     REFERENCES dim_dates(date_key)
)
''')

conn.commit()
conn.close()
print("✅ Database created: data/processed/health_analytics.db")
print("Tables created: dim_countries, dim_dates, dim_diseases,")
print("                fact_disease_cases, fact_vaccination_rates, fact_mortality")