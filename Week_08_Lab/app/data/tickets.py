import pandas as pd
from .db import connect_database

def load_csv_to_table(csv_path, table_name):
    if not Path(csv_path).exists():
        print(f"{csv_path} not found!")
        return 0
    conn = connect_database()
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, conn, if_exists='append', index=False)
    rows = len(df)
    print(f"Loaded {rows} rows into {table_name}")
    conn.close()
    return rows