import os, json, glob, sqlite3, pandas as pd

def parse_aggregated_insurance(base_path, conn):
    folder = os.path.join(base_path, "aggregated/insurance/country/india/state")
    files = glob.glob(os.path.join(folder, "*/*/*.json"))
    rows = []

    for file in files:
        state = file.split("/")[-3]
        year = int(file.split("/")[-2])
        quarter = int(file.split("/")[-1].replace(".json",""))

        with open(file, "r") as f:
            data = json.load(f)

        if "data" in data and "transactionData" in data["data"]:
            for entry in data["data"]["transactionData"]:
                category = entry.get("name", "Unknown")
                for pi in entry.get("paymentInstruments", []):
                    if pi["type"] == "TOTAL":
                        rows.append([
                            state, year, quarter,
                            category, pi.get("count",0), pi.get("amount",0.0)
                        ])

    if rows:
        df = pd.DataFrame(rows, columns=["state","year","quarter","category","count","amount"])
        df.to_sql("aggregated_insurance", conn, if_exists="replace", index=False)
        print("✅ aggregated_insurance loaded:", len(df), "rows")
    else:
        print("⚠️ No data found for aggregated_insurance")
