import os
from enum import Enum

RACE_INFO_DIR = os.environ.get("RACE_INFO_DIR")


DATABASE = os.environ.get("DATABASE")


swagger_config = {
    'title': 'My API'
}


class OrderEnum(str, Enum):
    desc = "desc"
    asc = "asc"


class FormatEnum(str, Enum):
    json = "json"
    xml = "xml"
