from peewee import SqliteDatabase

from my_app.my_settings.constants import DATABASE

db = SqliteDatabase(DATABASE)
