import os

from peewee import SqliteDatabase

db = SqliteDatabase(os.environ.get("DATABASE"))
