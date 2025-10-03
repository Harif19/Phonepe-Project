
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

# 4. Most popular payment categories
Q4 = """
SELECT category, SUM(count) AS total_count, SUM(amount) AS total_amount
FROM aggregated_transaction
GROUP BY category
ORDER BY total_amount DESC;
"""

# 5. Category-wise distribution in latest year (2023)
Q5 = """
SELECT category, SUM(amount) AS total_amount
FROM aggregated_transaction
WHERE year = 2023
GROUP BY category
ORDER BY total_amount DESC;
"""

def run_all(conn):
    results = {}
    results["Top 10 States by Amount"] = utils.run_query(conn, Q1)
    results["Yearly Trend"] = utils.run_query(conn, Q2)
    results["Quarterly Growth - Karnataka"] = utils.run_query(conn, Q3)
    results["Popular Payment Categories"] = utils.run_query(conn, Q4)
    results["2023 Category Distribution"] = utils.run_query(conn, Q5)
    return results
