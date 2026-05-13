-- ══════════════════════════════════════════════════════════
-- GLOBAL HEALTH ANALYTICS - SQL ANALYSIS QUERIES
-- ══════════════════════════════════════════════════════════


-- ── QUERY 1: Top 10 countries by total deaths ─────────────
SELECT
    c.country_name,
    c.region,
    SUM(f.deaths_count)    AS total_deaths,
    SUM(f.cases_count)     AS total_cases,
    ROUND(SUM(f.deaths_count) * 100.0 / NULLIF(SUM(f.cases_count), 0), 2) AS fatality_rate_pct
FROM fact_disease_cases f
JOIN dim_countries c ON f.country_key = c.country_key
GROUP BY c.country_name, c.region
ORDER BY total_deaths DESC
LIMIT 10;


-- ── QUERY 2: Deaths by continent/region ───────────────────
SELECT
    c.region,
    COUNT(DISTINCT c.country_key)  AS country_count,
    SUM(f.deaths_count)            AS total_deaths,
    SUM(f.cases_count)             AS total_cases,
    ROUND(AVG(f.case_fatality_rate), 2) AS avg_fatality_rate
FROM fact_disease_cases f
JOIN dim_countries c ON f.country_key = c.country_key
WHERE c.region IS NOT NULL
GROUP BY c.region
ORDER BY total_deaths DESC;


-- ── QUERY 3: Monthly death trends (global) ────────────────
SELECT
    d.year,
    d.month,
    SUM(f.deaths_count)  AS monthly_deaths,
    SUM(f.cases_count)   AS monthly_cases
FROM fact_disease_cases f
JOIN dim_dates d ON f.date_key = d.date_key
GROUP BY d.year, d.month
ORDER BY d.year, d.month;


-- ── QUERY 4: Vaccination progress by region ───────────────
SELECT
    c.region,
    COUNT(DISTINCT c.country_key)          AS countries,
    ROUND(MAX(v.vaccination_rate), 2)      AS max_vax_rate,
    ROUND(AVG(v.vaccination_rate), 2)      AS avg_vax_rate,
    ROUND(MIN(v.vaccination_rate), 2)      AS min_vax_rate
FROM fact_vaccination_rates v
JOIN dim_countries c ON v.country_key = c.country_key
WHERE v.vaccination_rate IS NOT NULL
  AND c.region IS NOT NULL
GROUP BY c.region
ORDER BY avg_vax_rate DESC;


-- ── QUERY 5: Top 10 most vaccinated countries ─────────────
SELECT
    c.country_name,
    c.region,
    ROUND(MAX(v.vaccination_rate), 2)  AS vaccination_rate_pct,
    MAX(v.fully_vaccinated)            AS fully_vaccinated
FROM fact_vaccination_rates v
JOIN dim_countries c ON v.country_key = c.country_key
WHERE v.vaccination_rate IS NOT NULL
GROUP BY c.country_name, c.region
ORDER BY vaccination_rate_pct DESC
LIMIT 10;


-- ── QUERY 6: Worst mortality rate per million ─────────────
SELECT
    c.country_name,
    c.region,
    ROUND(MAX(m.mortality_rate), 2)  AS mortality_per_million,
    SUM(m.deaths_count)              AS total_deaths
FROM fact_mortality m
JOIN dim_countries c ON m.country_key = c.country_key
WHERE m.mortality_rate IS NOT NULL
GROUP BY c.country_name, c.region
ORDER BY mortality_per_million DESC
LIMIT 10;


-- ── QUERY 7: Yearly case summary ──────────────────────────
SELECT
    d.year,
    SUM(f.cases_count)   AS yearly_cases,
    SUM(f.deaths_count)  AS yearly_deaths,
    ROUND(SUM(f.deaths_count) * 100.0 / NULLIF(SUM(f.cases_count), 0), 2) AS fatality_rate_pct
FROM fact_disease_cases f
JOIN dim_dates d ON f.date_key = d.date_key
GROUP BY d.year
ORDER BY d.year;


-- ── QUERY 8: Countries with low vaccination + high deaths ─
SELECT
    c.country_name,
    c.region,
    ROUND(MAX(v.vaccination_rate), 2)  AS max_vax_rate,
    SUM(f.deaths_count)                AS total_deaths
FROM fact_disease_cases f
JOIN dim_countries c      ON f.country_key = c.country_key
LEFT JOIN fact_vaccination_rates v ON f.country_key = v.country_key
GROUP BY c.country_name, c.region
HAVING max_vax_rate < 40 AND total_deaths > 1000
ORDER BY total_deaths DESC;


-- ── QUERY 9: Peak death day per country (top 10) ──────────
SELECT
    c.country_name,
    d.full_date        AS peak_date,
    f.deaths_count     AS peak_daily_deaths
FROM fact_disease_cases f
JOIN dim_countries c ON f.country_key = c.country_key
JOIN dim_dates d      ON f.date_key = d.date_key
WHERE f.deaths_count = (
    SELECT MAX(f2.deaths_count)
    FROM fact_disease_cases f2
    WHERE f2.country_key = f.country_key
)
ORDER BY peak_daily_deaths DESC
LIMIT 10;


-- ── QUERY 10: Quarterly global trend ─────────────────────
SELECT
    d.year,
    d.quarter,
    SUM(f.cases_count)   AS quarterly_cases,
    SUM(f.deaths_count)  AS quarterly_deaths
FROM fact_disease_cases f
JOIN dim_dates d ON f.date_key = d.date_key
GROUP BY d.year, d.quarter
ORDER BY d.year, d.quarter;