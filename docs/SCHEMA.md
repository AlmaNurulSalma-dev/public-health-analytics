# Database Schema

## Overview
Star schema design with 3 dimension tables and 3 fact tables.

## Dimension Tables

### dim_countries
| Column | Type | Description |
|--------|------|-------------|
| country_key | INTEGER PK | Surrogate key |
| country_name | TEXT | Full country name |
| iso_code | TEXT | 3-letter ISO code |
| region | TEXT | Geographic continent |
| population | INTEGER | Total population |
| income_level | TEXT | World Bank income level |

### dim_dates
| Column | Type | Description |
|--------|------|-------------|
| date_key | INTEGER PK | YYYYMMDD format |
| full_date | TEXT | ISO date string |
| year | INTEGER | Year |
| month | INTEGER | Month (1-12) |
| day | INTEGER | Day (1-31) |
| quarter | INTEGER | Quarter (1-4) |

### dim_diseases
| Column | Type | Description |
|--------|------|-------------|
| disease_key | INTEGER PK | Surrogate key |
| disease_name | TEXT | Disease name |
| disease_category | TEXT | Infectious/Chronic |
| is_communicable | INTEGER | 1=Yes, 0=No |

## Fact Tables

### fact_disease_cases
| Column | Type | Description |
|--------|------|-------------|
| case_key | INTEGER PK | Surrogate key |
| country_key | INTEGER FK | Links to dim_countries |
| disease_key | INTEGER FK | Links to dim_diseases |
| date_key | INTEGER FK | Links to dim_dates |
| cases_count | REAL | Daily new cases |
| deaths_count | REAL | Daily new deaths |
| case_fatality_rate | REAL | CFR percentage |

### fact_vaccination_rates
| Column | Type | Description |
|--------|------|-------------|
| vaccination_key | INTEGER PK | Surrogate key |
| country_key | INTEGER FK | Links to dim_countries |
| disease_key | INTEGER FK | Links to dim_diseases |
| date_key | INTEGER FK | Links to dim_dates |
| people_vaccinated | REAL | Cumulative vaccinated |
| fully_vaccinated | REAL | Fully vaccinated |
| vaccination_rate | REAL | Rate per hundred |

### fact_mortality
| Column | Type | Description |
|--------|------|-------------|
| mortality_key | INTEGER PK | Surrogate key |
| country_key | INTEGER FK | Links to dim_countries |
| disease_key | INTEGER FK | Links to dim_diseases |
| date_key | INTEGER FK | Links to dim_dates |
| deaths_count | REAL | Daily deaths |
| mortality_rate | REAL | Deaths per million |

## Record Counts
| Table | Records |
|-------|---------|
| dim_countries | 63 |
| dim_dates | 2,245 |
| dim_diseases | 1 |
| fact_disease_cases | 139,555 |
| fact_vaccination_rates | 18,125 |
| fact_mortality | 138,243 |