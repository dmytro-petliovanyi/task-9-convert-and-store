from typer.testing import CliRunner

from my_app.db.models import all_models
from my_app.db.repository import DriversRepository
from script_start import fill_app
from test_my_app.conftest import drivers_query_for_tests, racers_for_patch


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(fill_app, ["--help"])
    assert result.exit_code == 0


def test_cli_fill(db):
    DriversRepository.create_from_list(racers_for_patch)

    drivers = all_models[0].select()
    assert len(drivers) == 3


def test_cli_init(db):
    runner = CliRunner()
    result = runner.invoke(fill_app, ["init"])
    assert result.exit_code == 0
    for model in all_models:
        assert db.table_exists(model)


def test_repo_get(db):
    DriversRepository.create_from_list(racers_for_patch)

    result = DriversRepository.get()
    assert [driver for driver in result] == [driver for driver in drivers_query_for_tests]
    assert [driver.abbr for driver in result] == [driver.abbr for driver in drivers_query_for_tests]


def test_repo_get_single(db):
    DriversRepository.create_from_list(racers_for_patch)

    result = DriversRepository.get_single("SVF")
    assert result == drivers_query_for_tests[1]
    assert result == drivers_query_for_tests[1]


def test_repo_create_from_list(db):
    DriversRepository.create_from_list(racers_for_patch)

    result = DriversRepository.get()
    assert [driver for driver in result] == [driver for driver in drivers_query_for_tests]
    assert [driver.abbr for driver in result] == [driver.abbr for driver in drivers_query_for_tests]
