import os
from pathlib import Path

from peewee import SqliteDatabase

SQLITE_SCHEMA = Path(os.path.abspath(f"{__path__[0]}/../../db/arc.sql"))
SQLITE_DATABASE = Path(os.path.abspath(f"{__path__[0]}/../../db/arc.db"))

IMPORT_DATA_DIRECTORY = Path(os.path.abspath(f"{__path__[0]}/../../db/import/"))

db = SqliteDatabase(SQLITE_DATABASE)