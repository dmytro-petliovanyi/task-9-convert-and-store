import logging
import os

from report_of_monaco_racing import Racer, groper

from my_app.functions_view import get_abbr
from my_app.models import DriverModel, db

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.StreamHandler()]
)


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


if __name__ == "__main__":
    fill_driver_table(groper(os.environ.get("RACE_INFO_DIR")))
