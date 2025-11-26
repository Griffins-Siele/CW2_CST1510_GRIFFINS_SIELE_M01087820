import pandas as pd
from pathlib import Path 
from .db import connect_database

def load_csv_to_table(csv_path, table_name):
    """Load a CSV file into the database using pandas.

    Returns number of rows loaded, or 0 on failure.
    """
    csv_full_path = Path(csv_path)
    
    if not csv_full_path.exists():
        print(f"Warning: File not found: {csv_full_path}")
        return 0

    conn = connect_database()
    try:
        df = pd.read_csv(csv_full_path)
        df.to_sql(table_name, conn, if_exists='append', index=False)
        print(f"Success: Loaded {len(df)} rows → {table_name}")
        return len(df)
    except Exception as e:
        print(f"Error loading {csv_path}: {e}")
        return 0
    finally:
        conn.close()