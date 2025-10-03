"""
Case Study 2: Device Dominance and User Engagement
--------------------------------------------------
This case study analyzes:
1. Top device brands overall
2. Yearly app opens trend
3. Device distribution in the top state (latest valid year)
4. Top states by registered users (latest year)
5. Xiaomi quarterly growth trend
"""

import sqlite3
import utils

DB_PATH = "/content/project_files/phonepe_pulse.db"

# 1. Top 10 device brands across all years
Q1 = """
SELECT brand, SUM(count) AS total_users
FROM aggregated_user
WHERE brand != 'TOTAL'
GROUP BY brand
ORDER BY total_users DESC
LIMIT 10;
"""

# 2. Yearly growth of app opens
Q2 = """
SELECT year, SUM(percentage) AS total_app_opens
FROM aggregated_user
WHERE brand = 'TOTAL'
GROUP BY year
ORDER BY year;
"""

# 3. Device distribution for the top state (latest valid year with device rows)
Q3 = """
WITH top_state AS (
    SELECT state
    FROM aggregated_user
    WHERE brand = 'TOTAL'
    GROUP BY state
    ORDER BY SUM(count) DESC
    LIMIT 1
),
latest_valid_year AS (
    SELECT year
    FROM aggregated_user au
    JOIN top_state ts ON au.state = ts.state
    WHERE au.brand != 'TOTAL'
    GROUP BY year
    ORDER BY year DESC
    LIMIT 1
)
SELECT au.state, au.year, au.brand, SUM(au.count) AS total_users
FROM aggregated_user au
JOIN top_state ts ON au.state = ts.state
JOIN latest_valid_year lv ON au.year = lv.year
WHERE au.brand != 'TOTAL'
GROUP BY au.state, au.year, au.brand
ORDER BY total_users DESC;
"""

# 4. Top 5 states by registered users (latest year)
Q4 = """
SELECT state, SUM(count) AS total_users
FROM aggregated_user
WHERE brand = 'TOTAL'
  AND year = (SELECT MAX(year) FROM aggregated_user)
GROUP BY state
ORDER BY total_users DESC
LIMIT 5;
"""

# 5. Xiaomi quarterly trend
Q5 = """
SELECT year, quarter, SUM(count) AS xiaomi_users
FROM aggregated_user
WHERE brand = 'Xiaomi'
GROUP BY year, quarter
ORDER BY year, quarter;
"""

def run_all(db_path=DB_PATH):
    """
    Runs all 5 queries and returns results as a dictionary of DataFrames
    """
    conn = sqlite3.connect(db_path)
    results = {}
    results["Top Device Brands (All Years)"] = utils.run_query(conn, Q1)
    results["Yearly App Opens (All India)"] = utils.run_query(conn, Q2)
    results["Device Distribution in Top State (Latest Valid Year)"] = utils.run_query(conn, Q3)
    results["Top States by Registered Users (Latest Year)"] = utils.run_query(conn, Q4)
    results["Xiaomi Quarterly Trend (All India)"] = utils.run_query(conn, Q5)
    conn.close()
    return results
