import datetime
from typing import Generator

import pytest
from flask.testing import FlaskClient
from peewee import SqliteDatabase
from report_of_monaco_racing import Racer

from my_app import app
from my_app.api import api  # noqa
from my_app.db.models import DriverModel, all_models
from my_app.db.repository import DriversRepository
from my_app.functions_view import get_abbr
from my_app.my_settings.config import TestConfig

racers_for_patch = [
        Racer(
            'Daniel Ricciardo',
            'RED BULL RACING TAG HEUER',
            datetime.time(12, 14, 12, 54000),
            datetime.time(12, 11, 24, 67000)
        ),
        Racer(
            'Sebastian Vettel',
            'FERRARI',
            datetime.time(12, 2, 58, 917000),
            datetime.time(12, 4, 3, 332000)
        ),
        Racer(
            'Lewis Hamilton',
            'MERCEDES',
            datetime.time(12, 18, 20, 125000),
            datetime.time(12, 11, 32, 585000)
        )
    ]


full_list_of_dict_for_test_with_place = [
    {
        "abbr": "SVF",
        "fullname": "Sebastian Vettel",
        "place": 1,
        "team": "FERRARI",
        "time": "0:01:04.415000"
    },
    {
        "abbr": "DRR",
        "fullname": "Daniel Ricciardo",
        "place": 2,
        "team": "RED BULL RACING TAG HEUER",
        "time": "0:02:47.987000"
    },
    {
        "abbr": "LHM",
        "fullname": "Lewis Hamilton",
        "place": 3,
        "team": "MERCEDES",
        "time": "0:06:47.540000"
    }
]

full_list_of_dict_for_test_with_place_desc = [
    {
        "abbr": "LHM",
        "fullname": "Lewis Hamilton",
        "place": 1,
        "team": "MERCEDES",
        "time": "0:06:47.540000"
    },
    {
        "abbr": "DRR",
        "fullname": "Daniel Ricciardo",
        "place": 2,
        "team": "RED BULL RACING TAG HEUER",
        "time": "0:02:47.987000"
    },
    {
        "abbr": "SVF",
        "fullname": "Sebastian Vettel",
        "place": 3,
        "team": "FERRARI",
        "time": "0:01:04.415000"
    },

]

full_list_of_dict_for_test = [
    {
        "abbr": get_abbr(racer),
        "fullname": racer.fullname,
        "team": racer.team,
        "time": str(racer.best_lap)
    } for racer in racers_for_patch
]

small_list_of_dict_for_test = [
    {
        "abbr": get_abbr(racer),
        "fullname": racer.fullname,
    }
    for racer in racers_for_patch
]

drivers_query_for_tests = [DriverModel(id=racers_for_patch.index(racer)+1,
                                       abbr=get_abbr(racer),
                                       fullname=racer.fullname,
                                       team=racer.team,
                                       time=racer.best_lap) for racer in racers_for_patch]


@pytest.fixture(scope="session")
def client() -> FlaskClient:
    app.config.from_object(TestConfig)
    with app.test_client() as client:
        return client


@pytest.fixture(scope="session")
def test_db() -> SqliteDatabase:
    db = SqliteDatabase(":memory:")
    with db.bind_ctx(all_models):
        yield db


@pytest.fixture(scope="function")
def db(test_db: SqliteDatabase) -> SqliteDatabase:
    test_db.create_tables(all_models)
    yield test_db
    test_db.drop_tables(all_models)


@pytest.fixture(scope="function")
def repo(db: SqliteDatabase) -> Generator[DriversRepository, None, None]:
    DriversRepository.model.bind(db, bind_refs=False, bind_backrefs=False)
    yield DriversRepository()
