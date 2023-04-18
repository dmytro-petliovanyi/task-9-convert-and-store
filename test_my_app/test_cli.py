from unittest.mock import patch

from typer.testing import CliRunner

from my_app.db.models import all_models
from script_start import fill_app
from test_my_app.conftest import drivers_query_for_tests, racers_for_patch


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(fill_app, ["--help"])
    assert result.exit_code == 0


@patch("my_app.db.fill_driver_table.groper", return_value=racers_for_patch)
def test_cli_fill(patch_groper, db):
    runner = CliRunner()
    result = runner.invoke(fill_app, ["fill"])
    assert result.exit_code == 0

    patch_groper.assert_called()

    drivers = all_models[0].select()
    assert len(drivers) == 3


def test_cli_init(db, repo):
    runner = CliRunner()
    result = runner.invoke(fill_app, ["init"])
    assert result.exit_code == 0
    for model in all_models:
        assert db.table_exists(model)


def test_repo_get(db, repo):
    repo.create_from_list(racers_for_patch)

    result = repo.get()
    assert [driver for driver in result] == [driver for driver in drivers_query_for_tests]
    assert [driver.abbr for driver in result] == [driver.abbr for driver in drivers_query_for_tests]


def test_repo_get_single(db, repo):
    repo.create_from_list(racers_for_patch)

    result = repo.get_single("SVF")
    assert result == drivers_query_for_tests[1]
    assert result == drivers_query_for_tests[1]


def test_repo_create_from_list(db, repo):
    repo.create_from_list(racers_for_patch)

    result = repo.get()
    assert [driver for driver in result] == [driver for driver in drivers_query_for_tests]
    assert [driver.abbr for driver in result] == [driver.abbr for driver in drivers_query_for_tests]
