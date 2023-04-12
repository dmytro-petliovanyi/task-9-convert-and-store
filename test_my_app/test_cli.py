from functools import wraps
from unittest.mock import patch

from peewee import SqliteDatabase
from typer.testing import CliRunner

from my_app.db.models import all_models
from my_app.db.repository import DriversRepository
from script_start import fill_app
from test_my_app.conftest import drivers_query_for_tests, racers_for_patch

test_db = SqliteDatabase(':memory:')


def use_test_database(fn):
    @wraps(fn)
    def inner():
        with test_db.bind_ctx(all_models):
            test_db.create_tables(all_models)
            try:
                fn()
            finally:
                test_db.drop_tables(all_models)
    return inner


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(fill_app, ["--help"])
    assert result.exit_code == 0


@use_test_database
@patch("my_app.db.fill_driver_table.groper", return_value=racers_for_patch)
def test_cli_fill(patch_groper):
    runner = CliRunner()
    result = runner.invoke(fill_app, ["fill"])
    assert result.exit_code == 0

    patch_groper.assert_called()

    drivers = all_models[0].select()
    assert len(drivers) == 3


@use_test_database
def test_cli_init():
    runner = CliRunner()
    result = runner.invoke(fill_app, ["init"])
    assert result.exit_code == 0
    for model in all_models:
        assert test_db.table_exists(model)


@use_test_database
@patch("my_app.db.fill_driver_table.groper", return_value=racers_for_patch)
def test_repo_get(patch_groper):
    runner = CliRunner()
    func_result = runner.invoke(fill_app, ["fill"])
    assert func_result.exit_code == 0

    patch_groper.assert_called()

    result = DriversRepository().get()
    assert [driver for driver in result] == [driver for driver in drivers_query_for_tests]
    assert [driver.abbr for driver in result] == [driver.abbr for driver in drivers_query_for_tests]


@use_test_database
@patch("my_app.db.fill_driver_table.groper", return_value=racers_for_patch)
def test_repo_get_single(patch_groper):
    runner = CliRunner()
    func_result = runner.invoke(fill_app, ["fill"])
    assert func_result.exit_code == 0

    patch_groper.assert_called()

    result = DriversRepository().get_single("SVF")
    assert result == drivers_query_for_tests[1]
    assert result == drivers_query_for_tests[1]
