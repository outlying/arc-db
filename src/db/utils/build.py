import csv
import logging

from peewee import *

from src.db import SQLITE_DATABASE, IMPORT_DATA_DIRECTORY
from src.db.consts import TABLE_ITEMS
from src.db.utils.mappers import MAPPERS

db = SqliteDatabase(SQLITE_DATABASE)

logger = logging.getLogger(__name__)

class BaseModel(Model):
    class Meta:
        database = db

class Item(BaseModel):
    slug = CharField()
    name = CharField()

    class Meta:
        table_name = TABLE_ITEMS

if __name__ == "__main__":

    logger.info("Starting database build")

    if SQLITE_DATABASE.exists():
        logger.info("Old database file removed")
        SQLITE_DATABASE.unlink()

    db.connect()
    db.create_tables([Item])

    for csv_path in IMPORT_DATA_DIRECTORY.glob("*.csv"):
        table_name = csv_path.stem
        logger.info(f"Importing data to '{table_name}' table")

        rows = []
        with open(csv_path, newline="", encoding="utf-8") as f:
            logger.info(f"File opened {csv_path}")
            reader = csv.DictReader(f)
            for r in reader:
                row = MAPPERS[table_name](r)
                rows.append(row)
            logger.info(f"Found {len(rows)} rows for import")

        result = Item.insert_many(rows).execute()
        if result != len(rows):
            logger.warning("Not all items were inserted")
        else:
            logger.info(f"All items successfully imported to {table_name}")