from peewee import Model, CharField, IntegerField, FloatField, Check

from src.db import db
from src.db.consts import TABLE_ITEMS

RARITY = ['common', 'uncommon', 'rare', 'epic', 'legendary']

# Fields

class RarityField(CharField):

    def db_value(self, value):
        if value not in RARITY:
            raise ValueError(f"Provided value '{value}' is not one of {RARITY}")
        return super().db_value(value)


# Models

class BaseModel(Model):
    class Meta:
        database = db

class Item(BaseModel):
    slug = CharField(unique=True)
    name = CharField()
    value = IntegerField(constraints=[
        Check('value > 0')
    ])
    weight = FloatField(constraints=[
        Check('weight > 0.0')
    ])
    stack_size = IntegerField(constraints=[
        Check('stack_size >= 1')
    ])
    rarity = RarityField()

    class Meta:
        table_name = TABLE_ITEMS

class Recycling(BaseModel):
    source_item_id = IntegerField()
    output_item_id = IntegerField()
    amount = IntegerField(constraints=[
        Check('amount >= 1')
    ])