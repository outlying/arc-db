import csv
import sqlite3

from src.db import SQLITE_DATABASE, SQLITE_SCHEMA, IMPORT_DATA_DIRECTORY


def recreate_db():

    if SQLITE_DATABASE.exists():
        SQLITE_DATABASE.unlink()

    conn = sqlite3.connect(SQLITE_DATABASE)

    with open(SQLITE_SCHEMA, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    conn.executescript(schema_sql)
    conn.commit()

    return conn

def load_csv_to_table(conn, csv_path, table_name):
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if not rows:
        return

    columns = rows[0].keys()
    col_list = ", ".join(columns)
    placeholders = ", ".join(["?"] * len(columns))
    sql = f"INSERT INTO {table_name} ({col_list}) VALUES ({placeholders})"

    values = [tuple(row[col] for col in columns) for row in rows]
    conn.executemany(sql, values)
    conn.commit()

if __name__ == "__main__":
    conn = recreate_db()

    for csv_path in IMPORT_DATA_DIRECTORY.glob("*.csv"):
        table_name = csv_path.stem
        print(f"Loading {csv_path} into {table_name}")
        load_csv_to_table(conn, csv_path, table_name)

    conn.close()
