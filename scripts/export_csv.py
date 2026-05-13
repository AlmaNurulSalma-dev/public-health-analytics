import sqlite3
import pandas as pd
import os

conn = sqlite3.connect('data/processed/health_analytics.db')

tables = ['dim_countries', 'dim_dates', 'fact_disease_cases', 'fact_vaccination_rates', 'fact_mortality']

for t in tables:
    df = pd.read_sql(f'SELECT * FROM {t}', conn)
    df.to_csv(f'data/processed/{t}.csv', index=False)
    print(f'✅ Exported {t} - {len(df)} rows')

conn.close()
print('\n🎉 All CSVs exported!')