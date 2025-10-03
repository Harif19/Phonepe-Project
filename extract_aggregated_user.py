"""
Extract Aggregated User JSON files into SQLite
Table: aggregated_user (with device-level + totals)
"""

import os, json, sqlite3, glob, pandas as pd

def parse_aggregated_user(base_path, conn):
    folder = os.path.join(base_path, "aggregated/user/country/india/state")
    files = glob.glob(os.path.join(folder, "*/*/*.json"))
    rows = []

    for file in files:
        state = file.split("/")[-3]
        year = int(file.split("/")[-2])
        quarter = int(file.split("/")[-1].replace(".json",""))

        with open(file, "r") as f:
            data = json.load(f)

        if "data" in data:
            # ✅ Device-level data
            if "usersByDevice" in data["data"] and data["data"]["usersByDevice"] is not None:
                for entry in data["data"]["usersByDevice"]:
                    rows.append([
                        state, year, quarter,
                        entry.get("brand"),
                        entry.get("count"),
                        entry.get("percentage"),
                        None,   # registeredUsers
                        None    # appOpens
                    ])

            # ✅ Aggregated totals
            if "aggregated" in data["data"] and data["data"]["aggregated"] is not None:
                agg = data["data"]["aggregated"]
                rows.append([
                    state, year, quarter,
                    "TOTAL",
                    None,                 # count not used here
                    None,                 # percentage not used here
                    agg.get("registeredUsers"),
                    agg.get("appOpens")
                ])

    if rows:
        df = pd.DataFrame(rows, columns=[
            "state","year","quarter","brand","count","percentage","registeredUsers","appOpens"
        ])
        df.to_sql("aggregated_user", conn, if_exists="replace", index=False)
        print("✅ aggregated_user loaded:", len(df), "rows")
    else:
        print("⚠️ No data found for aggregated_user")

def build_db(db_path="/content/project_files/phonepe_pulse.db", base_path="/content/pulse/data"):
    conn = sqlite3.connect(db_path)
    parse_aggregated_user(base_path, conn)
    return conn
