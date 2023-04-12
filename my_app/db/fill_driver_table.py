import typer
from peewee import IntegrityError
from report_of_monaco_racing import groper

from logging_config import logging
from my_app.functions_view import get_abbr
from my_app.my_settings.constants import DIR_RACE_INFO

from .models import all_models, db

fill_app = typer.Typer()


@fill_app.command("fill")
def fill_driver_table() -> None:
    model = all_models[0]
    db.create_tables([model])

    create_info = [{"abbr": get_abbr(driver),
                    "fullname": driver.fullname,
                    "team": driver.team,
                    "time": driver.best_lap} for driver in groper(DIR_RACE_INFO)]

    for item in create_info:
        try:
            model.insert(**item).execute()
            logging.info(f"Created row with id: {item} and driver_id: {item['abbr']}")
        except IntegrityError:
            logging.warning(f"Skipping duplicate entry with driver_id: {item['abbr']}")


@fill_app.command("init")
def init_driver_table() -> None:
    db.drop_tables(all_models)
    db.create_tables(all_models)

    logging.info("Tables ready")
