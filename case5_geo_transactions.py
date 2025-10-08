
"""
Case Study 5 – Geo-Based Transaction Insights
--------------------------------------------
Analyzes geographical trends and growth of transactions across India.
"""

import utils

# 1️⃣ Top States by Transaction Amount (Latest Year)
Q1 = """
SELECT state, SUM(amount) AS total_amount
FROM aggregated_transaction
WHERE year = (SELECT MAX(year) FROM aggregated_transaction)
GROUP BY state
ORDER BY total_amount DESC
LIMIT 10;
"""

# 2️⃣ Top Districts by Transaction Amount (Latest Year)
Q2 = """
SELECT entityName AS district, SUM(amount) AS total_amount
FROM top_transaction
WHERE level = 'districts'
GROUP BY entityName
ORDER BY total_amount DESC
LIMIT 10;
"""

# 3️⃣ Fastest-Growing States by Transaction Value (2022 → 2023)
Q3 = """
WITH yearly_data AS (
    SELECT state, year, SUM(amount) AS total_amount
    FROM aggregated_transaction
    WHERE year IN (2022, 2023)
    GROUP BY state, year
),
pivoted AS (
    SELECT
        state,
        SUM(CASE WHEN year = 2022 THEN total_amount ELSE 0 END) AS amt_2022,
        SUM(CASE WHEN year = 2023 THEN total_amount ELSE 0 END) AS amt_2023
    FROM yearly_data
    GROUP BY state
)
SELECT
    state,
    ROUND(amt_2022/10000000, 2) AS amount_2022_cr,
    ROUND(amt_2023/10000000, 2) AS amount_2023_cr,
    ROUND(((amt_2023 - amt_2022) * 100.0 / NULLIF(amt_2022, 0)), 2) AS growth_percent
FROM pivoted
ORDER BY growth_percent DESC
LIMIT 10;
"""

# 4️⃣ Yearly Transaction Growth
Q4 = """
SELECT year, SUM(amount) AS yearly_amount
FROM aggregated_transaction
GROUP BY year
ORDER BY year;
"""

# 5️⃣ State Contribution Share (Latest Year)
Q5 = """
WITH total AS (
    SELECT SUM(amount) AS national_total
    FROM aggregated_transaction
    WHERE year = (SELECT MAX(year) FROM aggregated_transaction)
)
SELECT
    state,
    SUM(amount) AS state_total,
    ROUND(SUM(amount)*100.0/(SELECT national_total FROM total),2) AS contribution_percent
FROM aggregated_transaction
WHERE year = (SELECT MAX(year) FROM aggregated_transaction)
GROUP BY state
ORDER BY state_total DESC
LIMIT 10;
"""

def run_all(conn):
    results = {}
    results["Top States by Transaction Amount (Latest Year)"] = utils.run_query(conn, Q1)
    results["Top Districts by Transaction Amount (Latest Year)"] = utils.run_query(conn, Q2)
    results["Fastest-Growing States by Transaction Value (2022 → 2023)"] = utils.run_query(conn, Q3)
    results["Yearly Transaction Growth"] = utils.run_query(conn, Q4)
    results["State Contribution Share (Latest Year)"] = utils.run_query(conn, Q5)
    return results
