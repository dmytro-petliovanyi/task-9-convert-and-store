import os
from typing import Optional

from dotenv import load_dotenv
from report_of_monaco_racing import groper

from my_app.functions_view import get_abbr
from my_app.models import DriverModel


def fill_driver_table(path: Optional[str]):
    for driver in groper(path):
        new_driver = DriverModel(abbr=get_abbr(driver),
                                 fullname=driver.fullname,
                                 team=driver.team,
                                 time=driver.best_lap)

        existing_driver = DriverModel.get_or_none(DriverModel.abbr == new_driver.abbr)

        if existing_driver:
            existing_driver.fullname = new_driver.fullname
            existing_driver.team = new_driver.team
            existing_driver.time = new_driver.time

        else:
            new_driver.save()


if __name__ == "__main__":
    load_dotenv()
    fill_driver_table(os.environ.get("RACE_INFO_DIR"))
    query = sorted(DriverModel.select(), key=lambda x: x.time)
    for driver in query:
        print(driver.abbr)
