"""
Case Study 1: Decoding Transaction Dynamics on PhonePe
Contains 5 SQL queries with helper functions
"""

import utils

# 1. Top 10 states by transaction amount
Q1 = """
SELECT state, SUM(amount) AS total_amount
FROM aggregated_transaction
GROUP BY state
ORDER BY total_amount DESC
LIMIT 10;
"""

# 2. Yearly trend of total transactions
Q2 = """
SELECT year, SUM(amount) AS yearly_amount
FROM aggregated_transaction
GROUP BY year
ORDER BY year;
"""

# 3. Quarterly growth of transactions in a state (example: Karnataka)
Q3 = """
SELECT state, year, quarter, SUM(amount) AS total_amount
FROM aggregated_transaction
WHERE state = 'karnataka'
GROUP BY state, year, quarter
ORDER BY year, quarter;
"""

# 4. Category growth & share by year
Q4 = """
SELECT
    category,
    year,
    ROUND(SUM(amount)/10000000, 2) AS total_amount_cr,
    ROUND(SUM(amount) * 100.0 / SUM(SUM(amount)) OVER (PARTITION BY year), 2) AS category_share_percent
FROM aggregated_transaction
GROUP BY category, year
ORDER BY year, total_amount_cr DESC;
"""

# 5. Emerging categories (2023 vs 2022)
Q5 = """
WITH yearly_data AS (
    SELECT category, year, SUM(amount) AS total_amount
    FROM aggregated_transaction
    WHERE year IN (2022, 2023)
    GROUP BY category, year
),
pivoted AS (
    SELECT
        category,
        SUM(CASE WHEN year = 2022 THEN total_amount ELSE 0 END) AS amt_2022,
        SUM(CASE WHEN year = 2023 THEN total_amount ELSE 0 END) AS amt_2023
    FROM yearly_data
    GROUP BY category
)
SELECT
    category,
    amt_2022/10000000 AS amount_2022_cr,
    amt_2023/10000000 AS amount_2023_cr,
    ROUND(((amt_2023 - amt_2022) * 100.0 / NULLIF(amt_2022, 0)), 2) AS growth_percent
FROM pivoted
ORDER BY growth_percent DESC
LIMIT 10;
"""

def run_all(conn):
    results = {}
    results["Top 10 States by Amount"] = utils.run_query(conn, Q1)
    results["Yearly Trend"] = utils.run_query(conn, Q2)
    results["Quarterly Growth - Karnataka"] = utils.run_query(conn, Q3)
    results["Category Growth & Share by Year"] = utils.run_query(conn, Q4)
    results["Emerging Categories (2023 vs 2022)"] = utils.run_query(conn, Q5)
    return results
