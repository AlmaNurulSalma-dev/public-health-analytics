# Global Health Analytics Platform

End-to-end analytics platform for global COVID-19 health metrics using 
real data from Our World in Data (WHO/CDC sourced).

## 📊 Project Overview

| Item | Details |
|------|---------|
| **Data Source** | Our World in Data (WHO/CDC) |
| **Countries** | 63 countries |
| **Records** | 139,555+ |
| **Time Period** | 2020-2026 |
| **Cost** | 100% FREE |

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python (pandas) | ETL pipeline |
| SQLite | Local database |
| SQL | Analysis queries |
| Power BI Desktop | Dashboards |
| Git/GitHub | Version control |

## 🗄️ Database Schema

Star schema with 6 tables:
- **3 Dimension tables:** countries, dates, diseases
- **3 Fact tables:** disease cases, vaccination rates, mortality

## 📈 Dashboards (5 Pages)

1. **Global Overview** — KPI cards, deaths by region, trends
2. **Disease Tracking** — Cases/deaths over time, scatter analysis
3. **Vaccination Progress** — Coverage by country and region
4. **Health Disparities** — Regional mortality comparisons
5. **Comparative Analysis** — Country benchmarking

## 🔍 Key Insights

- 🇧🇷 **Brazil** had highest total deaths (703,774)
- 🇧🇬 **Bulgaria** had worst mortality per million (5,681)
- 🌎 **South America** was hardest hit region (1.1M deaths)
- 📉 **CFR dropped from 2.56% → 0.19%** (2020→2022) — vaccines working
- 🇧🇳 **Brunei** best recovery — 350k cases, only 182 deaths (0.05% CFR)
- 🇨🇳 **China** had 239,000% case growth 2021→2022 (zero-covid policy ended)
- 💉 **Cook Islands** most vaccinated at 102% (boosters counted)

## 🚀 Quick Start

```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/public-health-analytics.git
cd public-health-analytics

# Setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Run ETL
python scripts/create_database.py
python scripts/load_data.py
python scripts/export_csv.py

# Run analysis
python scripts/run_queries.py
python scripts/run_advanced_queries.py
```

## 📁 Project Structure
public-health-analytics/
├── data/
│   ├── raw/              # CSV downloads
│   └── processed/        # SQLite database + exported CSVs
├── scripts/
│   ├── create_database.py
│   ├── load_data.py
│   ├── export_csv.py
│   ├── run_queries.py
│   ├── analysis_queries.sql
│   ├── run_advanced_queries.py
│   └── advanced_queries.sql
├── dashboards/
│   └── health_analytics.pbix
├── docs/
│   ├── DATA_SOURCES.md
│   ├── SCHEMA.md
│   └── SETUP_GUIDE.md
├── requirements.txt
└── README.md

## 🎓 Interview Story

> "I built a global health analytics platform integrating real COVID-19 
> data from WHO and CDC via Our World in Data. I created Python ETL 
> pipelines to fetch and transform data for 63 countries, designed a 
> star schema SQLite database with 139k+ records, and wrote 20+ SQL 
> queries analyzing disease trends, vaccination effectiveness, and 
> health disparities. I built 5 interactive Power BI dashboards and 
> identified key insights like the CFR dropping from 2.56% to 0.19% 
> as vaccines rolled out."

## 📚 Documentation

- [Data Sources](docs/DATA_SOURCES.md)
- [Database Schema](docs/SCHEMA.md)
- [Setup Guide](docs/SETUP_GUIDE.md)