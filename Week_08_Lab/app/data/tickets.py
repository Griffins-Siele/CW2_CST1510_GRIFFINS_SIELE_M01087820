from pathlib import Path
from .datasets import load_csv_to_table as load_csv_to_table_from_datasets

def load_csv_to_table(csv_path, table_name):
    """Proxy to the shared CSV loader in `datasets.py`.

    Keeps a single implementation for loading CSVs into the DB.
    """
    return load_csv_to_table_from_datasets(csv_path, table_name)