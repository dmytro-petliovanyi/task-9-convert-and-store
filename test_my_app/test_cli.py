from unittest.mock import patch

from typer.testing import CliRunner

from my_app.db.models import all_models
from script_start import fill_app
from test_my_app.conftest import racers_for_patch


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(fill_app, ["--help"])
    assert result.exit_code == 0


@patch("my_app.db.fill_driver_table.groper", return_value=racers_for_patch)
def test_cli_fill(db):
    runner = CliRunner()
    result = runner.invoke(fill_app, ["fill"])
    assert result.exit_code == 0
    drivers = all_models[0].select()
    assert len(drivers) == 3


def test_cli_init(db):
    runner = CliRunner()
    result = runner.invoke(fill_app, ["init"])
    assert result.exit_code == 0
    for model in all_models:
        assert db.table_exists(model)
