from typer.testing import CliRunner

from script_start import fill_app


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(fill_app, ["--help"])
    assert result.exit_code == 0


def test_cli_fill():
    runner = CliRunner()
    result = runner.invoke(fill_app, ["fill"])
    assert result.exit_code == 0


def test_cli_init():
    runner = CliRunner()
    result = runner.invoke(fill_app, ["init", "Driver"])
    assert result.exit_code == 0
