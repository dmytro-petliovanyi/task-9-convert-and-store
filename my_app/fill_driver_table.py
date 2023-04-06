from report_of_monaco_racing import Racer

from logging_config import logging

from .functions_view import get_abbr
from .work_with_db.models import DriverModel, db


def fill_driver_table(drivers: list[Racer]) -> None:
    db.drop_tables([DriverModel])
    db.create_tables([DriverModel])
    create_info = [{"abbr": get_abbr(driver),
                    "fullname": driver.fullname,
                    "team": driver.team,
                    "time": driver.best_lap} for driver in drivers]

    with db.atomic():
        DriverModel.insert_many(create_info).execute()

        query = DriverModel.select()
        for item in query:
            logging.info(f"Created row with id: {item} and driver_id:{item.abbr}")
