# Setup Guide

## Prerequisites
- Python 3.8+
- Power BI Desktop (free)
- Git

## Installation

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/public-health-analytics.git
cd public-health-analytics
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Download data
1. Go to https://ourworldindata.org/covid-deaths
2. Download Full Data CSV
3. Save as `data/raw/covid-deaths.csv`

### 5. Run ETL pipeline
```bash
# Create database schema
python scripts/create_database.py

# Load data
python scripts/load_data.py

# Export CSVs for Power BI
python scripts/export_csv.py
```

### 6. Run SQL queries
```bash
python scripts/run_queries.py
python scripts/run_advanced_queries.py
```

### 7. Open Power BI dashboard
1. Open Power BI Desktop
2. Open `dashboards/health_analytics.pbix`
3. Refresh data if needed

## Troubleshooting
- **ModuleNotFoundError**: Run `pip install -r requirements.txt`
- **Database locked**: Close Power BI then retry
- **CSV encoding error**: File is saved with `encoding='utf-8-sig'`