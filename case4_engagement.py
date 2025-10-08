
"""
Case Study 4: User Engagement & Growth Strategy
-----------------------------------------------
This case study analyzes:
1. Top states by registered users
2. Yearly growth of registered users
3. Quarterly trend of app opens in top state
4. Top districts by registered users
5. Engagement ratio (app opens vs registered users)
"""

import utils

# 1️⃣ Top states by registered users (latest year)
Q1 = """
SELECT state, year, SUM(count) AS total_users
FROM aggregated_user
WHERE brand = 'TOTAL'
  AND year = (SELECT MAX(year) FROM aggregated_user)
GROUP BY state, year
ORDER BY total_users DESC
LIMIT 10;
"""

# 2️⃣ Yearly growth of registered users nationwide
Q2 = """
SELECT year, SUM(count) AS yearly_users
FROM aggregated_user
WHERE brand = 'TOTAL'
GROUP BY year
ORDER BY year;
"""

# 3️⃣ Quarterly trend of app opens in the top state
Q3 = """
WITH top_state AS (
    SELECT state
    FROM aggregated_user
    WHERE brand = 'TOTAL'
    GROUP BY state
    ORDER BY SUM(count) DESC
    LIMIT 1
)
SELECT au.state, au.year, au.quarter, SUM(au.percentage) AS total_app_opens
FROM aggregated_user au
JOIN top_state ts ON au.state = ts.state
WHERE au.brand = 'TOTAL'
GROUP BY au.state, au.year, au.quarter
ORDER BY au.year, au.quarter;
"""

# 4️⃣ Top districts by registered users (latest year)
Q4 = """
SELECT district, year, SUM(registeredUsers) AS total_users
FROM map_user
WHERE year = (SELECT MAX(year) FROM map_user)
GROUP BY district, year
ORDER BY total_users DESC
LIMIT 10;
"""

# 5️⃣ Engagement ratio: App Opens / Registered Users (latest year, per state)
Q5 = """
SELECT state,
       SUM(count) AS total_registered_users,
       SUM(percentage) AS total_app_opens,
       ROUND(CAST(SUM(percentage) AS FLOAT)/SUM(count),2) AS engagement_ratio
FROM aggregated_user
WHERE brand = 'TOTAL'
  AND year = (SELECT MAX(year) FROM aggregated_user)
GROUP BY state
ORDER BY engagement_ratio DESC
LIMIT 10;
"""

def run_all(conn):
    """
    Runs all 5 queries and returns a dictionary of DataFrames
    """
    results = {}
    results["Top States by Registered Users (Latest Year)"] = utils.run_query(conn, Q1)
    results["Yearly Growth of Registered Users"] = utils.run_query(conn, Q2)
    results["Quarterly App Opens in Top State"] = utils.run_query(conn, Q3)
    results["Top Districts by Registered Users"] = utils.run_query(conn, Q4)
    results["Engagement Ratio by State (Latest Year)"] = utils.run_query(conn, Q5)
    return results
