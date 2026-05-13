import sqlite3
import os

db_path = os.path.join('data', 'processed', 'health_analytics.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

queries = {
    "Top 10 Countries by Deaths": '''
        SELECT c.country_name, c.region,
               SUM(f.deaths_count) AS total_deaths,
               ROUND(SUM(f.deaths_count)*100.0/NULLIF(SUM(f.cases_count),0),2) AS fatality_rate_pct
        FROM fact_disease_cases f
        JOIN dim_countries c ON f.country_key = c.country_key
        GROUP BY c.country_name, c.region
        ORDER BY total_deaths DESC LIMIT 10
    ''',
    "Deaths by Region": '''
        SELECT c.region, SUM(f.deaths_count) AS total_deaths,
               SUM(f.cases_count) AS total_cases
        FROM fact_disease_cases f
        JOIN dim_countries c ON f.country_key = c.country_key
        WHERE c.region IS NOT NULL
        GROUP BY c.region ORDER BY total_deaths DESC
    ''',
    "Top 10 Vaccinated Countries": '''
        SELECT c.country_name, ROUND(MAX(v.vaccination_rate),2) AS vax_rate_pct
        FROM fact_vaccination_rates v
        JOIN dim_countries c ON v.country_key = c.country_key
        WHERE v.vaccination_rate IS NOT NULL
        GROUP BY c.country_name
        ORDER BY vax_rate_pct DESC LIMIT 10
    ''',
    "Yearly Case Summary": '''
        SELECT d.year, SUM(f.cases_count) AS yearly_cases,
               SUM(f.deaths_count) AS yearly_deaths
        FROM fact_disease_cases f
        JOIN dim_dates d ON f.date_key = d.date_key
        GROUP BY d.year ORDER BY d.year
    ''',
    "Worst Mortality Rate per Million": '''
        SELECT c.country_name, ROUND(MAX(m.mortality_rate),2) AS mortality_per_million
        FROM fact_mortality m
        JOIN dim_countries c ON m.country_key = c.country_key
        WHERE m.mortality_rate IS NOT NULL
        GROUP BY c.country_name
        ORDER BY mortality_per_million DESC LIMIT 10
    '''
}

for title, query in queries.items():
    print(f"\n{'═'*55}")
    print(f"  {title}")
    print(f"{'═'*55}")
    cursor.execute(query)
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    print("  " + " | ".join(col_names))
    print("  " + "-" * 50)
    for row in rows:
        print("  " + " | ".join(str(x) for x in row))

conn.close()
print("\n✅ All queries complete!")