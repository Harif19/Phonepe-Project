"""
Case Study 5: Transaction Analysis Across States & Districts
------------------------------------------------------------
"""

import sqlite3
import utils

DB_PATH = "/content/project_files/phonepe_pulse.db"

# 1. Top states by transaction amount (latest year)
Q1 = """
SELECT state, SUM(amount) AS total_amount
FROM aggregated_transaction
WHERE year = (SELECT MAX(year) FROM aggregated_transaction)
GROUP BY state
ORDER BY total_amount DESC
LIMIT 10;
"""

# 2. Top districts by transaction amount (latest year)
Q2 = """
SELECT entityName AS district, SUM(amount) AS total_amount
FROM top_transaction
WHERE year = (SELECT MAX(year) FROM top_transaction)
  AND level = 'districts'
GROUP BY entityName
ORDER BY total_amount DESC
LIMIT 10;
"""

# 3. Top pincodes by transaction amount (latest year)
Q3 = """
SELECT entityName AS pincode, SUM(amount) AS total_amount
FROM top_transaction
WHERE year = (SELECT MAX(year) FROM top_transaction)
  AND level = 'pincodes'
GROUP BY entityName
ORDER BY total_amount DESC
LIMIT 10;
"""

# 4. Yearly transaction growth (nationwide)
Q4 = """
SELECT year, SUM(amount) AS yearly_amount
FROM aggregated_transaction
GROUP BY year
ORDER BY year;
"""

# 5. State contribution share (% of national total)
Q5 = """
WITH total AS (
    SELECT SUM(amount) AS national_total
    FROM aggregated_transaction
    WHERE year = (SELECT MAX(year) FROM aggregated_transaction)
)
SELECT state, SUM(amount) AS state_total,
       ROUND(SUM(amount)*100.0 / (SELECT national_total FROM total), 2) AS contribution_percent
FROM aggregated_transaction
WHERE year = (SELECT MAX(year) FROM aggregated_transaction)
GROUP BY state
ORDER BY state_total DESC
LIMIT 10;
"""

def run_all(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    results = {}
    results["Top States by Transaction Amount (Latest Year)"] = utils.run_query(conn, Q1)
    results["Top Districts by Transaction Amount (Latest Year)"] = utils.run_query(conn, Q2)
    results["Top Pincodes by Transaction Amount (Latest Year)"] = utils.run_query(conn, Q3)
    results["Yearly Transaction Growth"] = utils.run_query(conn, Q4)
    results["State Contribution Share (Latest Year)"] = utils.run_query(conn, Q5)
    conn.close()
    return results
