from peewee import CharField, Model, TimeField

from ..my_settings import db


class BaseModel(Model):
    class Meta:
        database = db


class DriverModel(BaseModel):
    abbr = CharField(unique=True)
    fullname = CharField()
    team = CharField()
    time = TimeField()


all_models = {"Driver": DriverModel}
