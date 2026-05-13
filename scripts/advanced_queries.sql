-- Query 11: Countries with highest case growth 2021 vs 2022
SELECT
    c.country_name,
    SUM(CASE WHEN d.year = 2021 THEN f.cases_count ELSE 0 END) AS cases_2021,
    SUM(CASE WHEN d.year = 2022 THEN f.cases_count ELSE 0 END) AS cases_2022,
    ROUND((SUM(CASE WHEN d.year = 2022 THEN f.cases_count ELSE 0 END) -
           SUM(CASE WHEN d.year = 2021 THEN f.cases_count ELSE 0 END)) * 100.0 /
           NULLIF(SUM(CASE WHEN d.year = 2021 THEN f.cases_count ELSE 0 END), 0), 2) AS growth_pct
FROM fact_disease_cases f
JOIN dim_countries c ON f.country_key = c.country_key
JOIN dim_dates d ON f.date_key = d.date_key
GROUP BY c.country_name
HAVING cases_2021 > 0
ORDER BY growth_pct DESC
LIMIT 10;

-- Query 12: Monthly vaccination rollout speed
SELECT
    d.year,
    d.month,
    SUM(v.people_vaccinated) AS monthly_vaccinated,
    SUM(v.people_vaccinated) - LAG(SUM(v.people_vaccinated))
        OVER (ORDER BY d.year, d.month) AS monthly_increase
FROM fact_vaccination_rates v
JOIN dim_dates d ON v.date_key = d.date_key
WHERE v.people_vaccinated IS NOT NULL
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

-- Query 13: Death rate improvement over years
SELECT
    d.year,
    ROUND(SUM(f.deaths_count) * 100.0 / NULLIF(SUM(f.cases_count), 0), 4) AS global_cfr
FROM fact_disease_cases f
JOIN dim_dates d ON f.date_key = d.date_key
GROUP BY d.year
ORDER BY d.year;

-- Query 14: Top 10 countries by total cases per million population
SELECT
    c.country_name,
    c.region,
    SUM(f.cases_count) AS total_cases,
    c.population,
    ROUND(SUM(f.cases_count) * 1000000.0 / NULLIF(c.population, 0), 2) AS cases_per_million
FROM fact_disease_cases f
JOIN dim_countries c ON f.country_key = c.country_key
WHERE c.population > 0
GROUP BY c.country_name, c.region, c.population
ORDER BY cases_per_million DESC
LIMIT 10;

-- Query 15: Vaccination rate vs death rate correlation
SELECT
    c.country_name,
    c.region,
    ROUND(MAX(v.vaccination_rate), 2) AS max_vax_rate,
    SUM(f.deaths_count) AS total_deaths
FROM dim_countries c
JOIN fact_vaccination_rates v ON c.country_key = v.country_key
JOIN fact_disease_cases f ON c.country_key = f.country_key
WHERE v.vaccination_rate IS NOT NULL
GROUP BY c.country_name, c.region
ORDER BY max_vax_rate DESC
LIMIT 15;

-- Query 16: Weekly death trend (last 3 months of peak year 2021)
SELECT
    d.full_date,
    SUM(f.deaths_count) AS daily_deaths,
    AVG(SUM(f.deaths_count)) OVER (
        ORDER BY d.full_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS rolling_7day_avg
FROM fact_disease_cases f
JOIN dim_dates d ON f.date_key = d.date_key
WHERE d.year = 2021 AND d.month >= 10
GROUP BY d.full_date
ORDER BY d.full_date;

-- Query 17: Countries that never had high death counts
SELECT
    c.country_name,
    c.region,
    SUM(f.deaths_count) AS total_deaths,
    MAX(f.deaths_count) AS peak_daily_deaths
FROM fact_disease_cases f
JOIN dim_countries c ON f.country_key = c.country_key
GROUP BY c.country_name, c.region
HAVING total_deaths < 1000
ORDER BY total_deaths ASC;

-- Query 18: Quarterly vaccination progress per region
SELECT
    c.region,
    d.year,
    d.quarter,
    ROUND(AVG(v.vaccination_rate), 2) AS avg_vax_rate,
    COUNT(DISTINCT c.country_key) AS countries_reporting
FROM fact_vaccination_rates v
JOIN dim_countries c ON v.country_key = c.country_key
JOIN dim_dates d ON v.date_key = d.date_key
WHERE v.vaccination_rate IS NOT NULL
  AND c.region IS NOT NULL
GROUP BY c.region, d.year, d.quarter
ORDER BY c.region, d.year, d.quarter;

-- Query 19: Peak pandemic month globally
SELECT
    d.year,
    d.month,
    SUM(f.cases_count) AS monthly_cases,
    SUM(f.deaths_count) AS monthly_deaths,
    COUNT(DISTINCT f.country_key) AS countries_affected
FROM fact_disease_cases f
JOIN dim_dates d ON f.date_key = d.date_key
GROUP BY d.year, d.month
ORDER BY monthly_cases DESC
LIMIT 5;

-- Query 20: Countries with best recovery (high cases, low deaths)
SELECT
    c.country_name,
    c.region,
    SUM(f.cases_count) AS total_cases,
    SUM(f.deaths_count) AS total_deaths,
    ROUND(SUM(f.deaths_count) * 100.0 / NULLIF(SUM(f.cases_count), 0), 4) AS cfr_pct
FROM fact_disease_cases f
JOIN dim_countries c ON f.country_key = c.country_key
GROUP BY c.country_name, c.region
HAVING total_cases > 100000
ORDER BY cfr_pct ASC
LIMIT 10;