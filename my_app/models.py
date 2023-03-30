from peewee import *


db = SqliteDatabase("../drivers_database.db")


class DriverModel(Model):
    abbr = CharField()
    fullname = CharField()
    team = CharField()
    time = TimeField()

    class Meta:
        database = db


db.create_tables([DriverModel])

