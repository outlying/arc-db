import re

from src.db.consts import TABLE_ITEMS

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text

def map_item(item):
    item["slug"] = slugify(item["name"])
    return item

MAPPERS = {
    TABLE_ITEMS: map_item
}