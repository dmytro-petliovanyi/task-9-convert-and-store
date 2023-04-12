from peewee import SqliteDatabase

from my_app.my_settings.constants import RACE_INFO_DIR

db = SqliteDatabase(RACE_INFO_DIR)
