import typer
from report_of_monaco_racing import groper

from logging_config import logging
from my_app.my_settings.constants import RACE_INFO_DIR

from .models import all_models, db
from .repository import DriversRepository

fill_app = typer.Typer()


@fill_app.command("fill")
def fill_driver_table() -> None:
    DriversRepository().create_from_list(
        groper(
            RACE_INFO_DIR
        )
    )


@fill_app.command("init")
def init_driver_table() -> None:
    db.drop_tables(all_models)
    db.create_tables(all_models)

    logging.info("Tables ready")
