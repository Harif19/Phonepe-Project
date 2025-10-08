
"""
Case Study 2: Device Dominance and User Engagement
--------------------------------------------------
This case study analyzes:
1. Top device brands overall
2. Yearly app opens trend
3. Device market share in the top state (latest valid year)
4. Top states by registered users (latest year)
5. Xiaomi quarterly growth trend
"""

import utils

# 1️⃣ Top 10 device brands across all years
Q1 = """
SELECT brand, SUM(count) AS total_users
FROM aggregated_user
WHERE brand != 'TOTAL'
GROUP BY brand
ORDER BY total_users DESC
LIMIT 10;
"""

# 2️⃣ Yearly growth of app opens
Q2 = """
SELECT year, SUM(percentage) AS total_app_opens
FROM aggregated_user
WHERE brand = 'TOTAL'
GROUP BY year
ORDER BY year;
"""

# 3️⃣ Device market share in the top state (latest valid year)
Q3 =  """WITH valid_year AS (
    SELECT MAX(year) AS yr
    FROM aggregated_user
    WHERE brand != 'TOTAL'
),
top_state AS (
    SELECT state
    FROM aggregated_user
    WHERE brand='TOTAL'
    GROUP BY state
    ORDER BY SUM(count) DESC
    LIMIT 1
)
SELECT au.state, au.brand, SUM(au.count) AS total_users,
       ROUND(SUM(au.count)*100.0 / SUM(SUM(au.count)) OVER(), 2) AS market_share_percent
FROM aggregated_user au
JOIN top_state ts ON au.state = ts.state
JOIN valid_year vy ON au.year = vy.yr
WHERE au.brand != 'TOTAL'
GROUP BY au.state, au.brand
ORDER BY total_users DESC;
"""
# 4️⃣ Top 5 states by registered users (latest year)
Q4 = """
SELECT state, SUM(count) AS total_users
FROM aggregated_user
WHERE brand = 'TOTAL'
  AND year = (SELECT MAX(year) FROM aggregated_user)
GROUP BY state
ORDER BY total_users DESC
LIMIT 5;
"""

# 5️⃣ Xiaomi quarterly trend
Q5 = """
SELECT year, quarter, SUM(count) AS xiaomi_users
FROM aggregated_user
WHERE brand = 'Xiaomi'
GROUP BY year, quarter
ORDER BY year, quarter;
"""

def run_all(conn):
    results = {}
    results["Top Device Brands (All Years)"] = utils.run_query(conn, Q1)
    results["Yearly App Opens (All India)"] = utils.run_query(conn, Q2)
    results["Device Market Share in Top State (Latest Year)"] = utils.run_query(conn, Q3)
    results["Top States by Registered Users (Latest Year)"] = utils.run_query(conn, Q4)
    results["Xiaomi Quarterly Trend (All India)"] = utils.run_query(conn, Q5)
    return results
