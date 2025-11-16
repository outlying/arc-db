import csv

import yaml
from ruamel.yaml import YAML
from ruamel.yaml.constructor import DuplicateKeyError
import logging

from src.db import SQLITE_DATABASE, IMPORT_DATA_DIRECTORY, db
from src.db.model import Item
from src.db.utils.mappers import MAPPERS

logger = logging.getLogger(__name__)

if __name__ == "__main__":

    logger.info("Starting database build")

    if SQLITE_DATABASE.exists():
        logger.info("Old database file removed")
        SQLITE_DATABASE.unlink()

    db.connect()
    db.create_tables([Item])

    yaml = YAML(typ="safe")
    yaml.allow_duplicate_keys = False

    # YAML import
    data: dict = dict()

    try:
        with open(IMPORT_DATA_DIRECTORY / "items.yml" ,"r", encoding="utf-8") as f:
            data = yaml.load(f)
    except DuplicateKeyError as e:
        logger.error(f"Duplicate key error {e}" )
        exit(1)

    

    # CSV import
    exit(0)

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
            logger.info(f"All rows successfully imported to '{table_name}' table")