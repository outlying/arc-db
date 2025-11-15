from peewee import Model, CharField

from src.db import db
from src.db.consts import TABLE_ITEMS


class BaseModel(Model):
    class Meta:
        database = db

class Item(BaseModel):
    slug = CharField()
    name = CharField()

    class Meta:
        table_name = TABLE_ITEMS