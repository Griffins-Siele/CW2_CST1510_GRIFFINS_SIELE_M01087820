from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import migrate_users_from_file, register_user, login_user
from app.data.incidents import insert_incident, get_all_incidents
from app.data.datasets import load_csv_to_table
from pathlib import Path

def setup_database_complete():
    print("SETTING UP DATABASE...")
    conn = connect_database()
    create_all_tables(conn)
    conn.close()

    migrate_users_from_file()

    # Load CSVs
    load_csv_to_table("DATA/cyber_incidents.csv", "cyber_incidents")
    load_csv_to_table("DATA/datasets_metadata.csv", "datasets_metadata")
    load_csv_to_table("DATA/it_tickets.csv", "it_tickets")

    print("DATABASE READY!")

if __name__ == "__main__":
    setup_database_complete()

    # Test authentication
    register_user("alice", "SecurePass123!", "analyst")
    success, msg = login_user("alice", "SecurePass123!")
    print(msg)

    # Test incident
    inc_id = insert_incident("2025-11-19", "Phishing", "High", "Open", "Fake email", "alice")
    print(f"Created incident #{inc_id}")

    df = get_all_incidents()
    print(f"\nTotal incidents: {len(df)}")
    print(df.head())