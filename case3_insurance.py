
"""
Case Study 3: Insurance Penetration & Growth Potential
------------------------------------------------------
Analyzes:
1. Top states by total insurance transaction amount
2. Yearly insurance growth trend
3. Quarterly trend in the top insurance state
4. Top insurance contributing states
5. Insurance penetration percentage across states
"""

import utils

# 1️⃣ Top states by total insurance transaction amount
Q1 = """
SELECT state, SUM(amount) AS total_insurance_amount
FROM aggregated_insurance
GROUP BY state
ORDER BY total_insurance_amount DESC
LIMIT 10;
"""

# 2️⃣ Yearly insurance growth trend
Q2 = """
SELECT year, SUM(amount) AS yearly_insurance_amount
FROM aggregated_insurance
GROUP BY year
ORDER BY year;
"""

# 3️⃣ Quarterly insurance trend in the top state
Q3 = """
WITH top_state AS (
    SELECT state
    FROM aggregated_insurance
    GROUP BY state
    ORDER BY SUM(amount) DESC
    LIMIT 1
)
SELECT ai.state, ai.year, ai.quarter, SUM(ai.amount) AS quarterly_amount
FROM aggregated_insurance ai
JOIN top_state ts ON ai.state = ts.state
GROUP BY ai.state, ai.year, ai.quarter
ORDER BY ai.year, ai.quarter;
"""

# 4️⃣ Top 5 states by insurance growth percentage (2020–2024)
Q4 = """
WITH yearly_state_amount AS (
    SELECT state, year, SUM(amount) AS yearly_amount
    FROM aggregated_insurance
    GROUP BY state, year
),
state_growth AS (
    SELECT state,
           MIN(yearly_amount) AS start_amount,
           MAX(yearly_amount) AS end_amount,
           ROUND(
               (CAST(MAX(yearly_amount) AS FLOAT) - MIN(yearly_amount)) / MIN(yearly_amount) * 100, 2
           ) AS growth_percent
    FROM yearly_state_amount
    GROUP BY state
    HAVING MIN(yearly_amount) > 0
)
SELECT state, growth_percent
FROM state_growth
ORDER BY growth_percent DESC
LIMIT 5;
"""


# 5️⃣ Insurance penetration: ratio of insurance to total transactions per state
Q5 = """
WITH insurance AS (
    SELECT state, SUM(amount) AS insurance_amount
    FROM aggregated_insurance
    GROUP BY state
),
transactions AS (
    SELECT state, SUM(amount) AS total_amount
    FROM aggregated_transaction
    GROUP BY state
)
SELECT t.state, insurance_amount, total_amount,
       ROUND(CAST(insurance_amount AS FLOAT)/total_amount*100,2) AS penetration_percent
FROM transactions t
LEFT JOIN insurance i ON t.state = i.state
ORDER BY penetration_percent DESC
LIMIT 10;
"""

def run_all(conn):
    """
    Runs all 5 insurance analysis queries and returns results as DataFrames.
    """
    results = {}
    results["Top States by Insurance Amount"] = utils.run_query(conn, Q1)
    results["Yearly Insurance Growth"] = utils.run_query(conn, Q2)
    results["Quarterly Trend in Top Insurance State"] = utils.run_query(conn, Q3)
    results["Top Insurance States (instead of Categories)"] = utils.run_query(conn, Q4)
    results["Insurance Penetration by State"] = utils.run_query(conn, Q5)
    return results
