import typer
from report_of_monaco_racing import groper

from logging_config import logging
from my_app.functions_view import get_abbr
from my_app.my_settings.constants import RACE_INFO_DIR

from .models import all_models, db
from .repository import DriversRepository

fill_app = typer.Typer()


@fill_app.command("fill")
def fill_driver_table() -> None:
    create_info = [{"abbr": get_abbr(driver),
                    "fullname": driver.fullname,
                    "team": driver.team,
                    "time": driver.best_lap} for driver in groper(RACE_INFO_DIR)]

    DriversRepository().create_from_list(create_info)


@fill_app.command("init")
def init_driver_table() -> None:
    db.drop_tables(all_models)
    db.create_tables(all_models)

    logging.info("Tables ready")
