import os

from dotenv import load_dotenv
from peewee import CharField, Model, SqliteDatabase, TimeField

load_dotenv()
db = SqliteDatabase(os.environ.get("DATABASE"))


class BaseModel(Model):
    class Meta:
        database = db


class DriverModel(BaseModel):
    abbr = CharField()
    fullname = CharField()
    team = CharField()
    time = TimeField()


db.create_tables([DriverModel])
