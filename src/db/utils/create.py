import sqlite3

from src.db import SQLITE_DATABASE, SQLITE_SCHEMA

if __name__ == "__main__":

    if SQLITE_DATABASE.exists():
        SQLITE_DATABASE.unlink()

    conn = sqlite3.connect(SQLITE_DATABASE)
    try:
        with open(SQLITE_SCHEMA, "r", encoding="utf-8") as f:
            schema_sql = f.read()
        conn.executescript(schema_sql)
        conn.commit()
    finally:
        conn.close()