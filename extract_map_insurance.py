
"""
Extract Aggregated Transaction JSON files into SQLite
Table: aggregated_transaction
"""

import os, json, sqlite3, glob, pandas as pd

def parse_aggregated_transaction(base_path, conn):
    folder = os.path.join(base_path, "aggregated/transaction/country/india/state")
    files = glob.glob(os.path.join(folder, "*/*/*.json"))
    rows = []

    for file in files:
        state = file.split("/")[-3]
        year = int(file.split("/")[-2])
        quarter = int(file.split("/")[-1].replace(".json",""))

        with open(file, "r") as f:
            data = json.load(f)

        if "data" in data and "transactionData" in data["data"] and data["data"]["transactionData"] is not None:
            for entry in data["data"]["transactionData"]:
                category = entry.get("name")
                for pi in entry.get("paymentInstruments", []):
                    rows.append([
                        state, year, quarter, category,
                        pi.get("type"), pi.get("count"), pi.get("amount")
                    ])

    if rows:
        df = pd.DataFrame(rows, columns=["state","year","quarter","category","type","count","amount"])
        df.to_sql("aggregated_transaction", conn, if_exists="replace", index=False)
        print("✅ aggregated_transaction loaded:", len(df), "rows")
    else:
        print("⚠️ No data found for aggregated_transaction")

def build_db(db_path="/content/project_files/phonepe_pulse.db", base_path="/content/pulse/data"):
    conn = sqlite3.connect(db_path)
    parse_aggregated_transaction(base_path, conn)
    return conn

if __name__ == "__main__":
    conn = build_db()
    print("Tables in DB:", conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
