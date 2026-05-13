 # Global Health Analytics Platform

End-to-end analytics platform for global COVID-19 health metrics using real data from Our World in Data (WHO/CDC sourced).

## Tech Stack
- Python (pandas, requests)
- SQLite
- SQL
- Power BI Desktop

## Data Source
- [Our World in Data](https://ourworldindata.org/) — COVID-19 dataset
- 63 countries, 2,245 dates, 139k+ records

## Key Insights
- Brazil had the highest total deaths (703,774) in this dataset
- Bulgaria had the worst mortality rate per million (5,681)
- South America was the hardest hit region (1.1M deaths)
- 2022 had the most cases (138M) but deaths dropped — vaccines working
- Cook Islands, Brunei, Cuba led vaccination rates (90%+)

## Project Structure
public-health-analytics/
├── data/
│   ├── raw/              # CSV downloads
│   └── processed/        # SQLite database
├── scripts/
│   ├── create_database.py
│   ├── load_data.py
│   ├── analysis_queries.sql
│   └── run_queries.py
├── dashboards/           # Power BI .pbix file
├── requirements.txt
└── README.md

## Setup
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python scripts\create_database.py
python scripts\load_data.py
python scripts\run_queries.py
```