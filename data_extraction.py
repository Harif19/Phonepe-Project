
import os, json, sqlite3, glob, pandas as pd

def find_repo_path(base_path=None):
    if base_path and os.path.exists(base_path):
        return base_path
    fallback = './pulse/data/aggregated/transaction/country/india/state'
    if os.path.exists(fallback):
        return fallback
    raise FileNotFoundError(f"Could not find PhonePe pulse data at {base_path or fallback}. Please clone the repo.")

def build_sqlite_db(base_path=None, db_path=':memory:', verbose=True):
    repo_path = find_repo_path(base_path)
    conn = sqlite3.connect(db_path)

    # Helper loader
    def load_json_files(glob_pattern):
        rows = []
        for fp in glob.glob(glob_pattern, recursive=True):
            try:
                with open(fp, 'r') as f:
                    data = json.load(f)
                if isinstance(data, dict) and 'data' in data and isinstance(data['data'], list):
                    for item in data['data']:
                        rows.append(item)
                elif isinstance(data, list):
                    rows.extend(data)
            except Exception as e:
                if verbose: print('skip', fp, e)
        if rows:
            return pd.json_normalize(rows, sep='_')
        return pd.DataFrame()

    tx_df = load_json_files(os.path.join(repo_path, '**', '*.json'))
    if not tx_df.empty:
        tx_df.to_sql('aggregated_transaction', conn, if_exists='replace', index=False)
        if verbose: print('Wrote aggregated_transaction:', tx_df.shape)

    # Placeholder tables
    conn.execute('CREATE TABLE IF NOT EXISTS map_user (state TEXT, year INTEGER, quarter INTEGER, registeredUsers INTEGER, appOpens INTEGER, device_brand TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS aggregated_insurance (state TEXT, year INTEGER, quarter INTEGER, insuranceValue REAL, insuranceCount INTEGER)')
    conn.commit()
    return conn

if __name__ == "__main__":
    conn = build_sqlite_db()
    print("Database built")
