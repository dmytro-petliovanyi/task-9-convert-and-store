from peewee import IntegrityError
from report_of_monaco_racing import Racer

from logging_config import logging
from my_app.functions_view import get_abbr

from .models import DriverModel, all_models, db


class DriversRepository:
    model = all_models[0]

    @classmethod
    def get(cls) -> list[DriverModel]:
        return cls.model.select()

    @classmethod
    def get_single(cls, abbr: str) -> DriverModel | None:
        return cls.model.get_or_none(DriverModel.abbr == abbr)

    @classmethod
    def create_from_list(cls, rows: list[Racer]):
        create_info = [cls.model(abbr=get_abbr(driver),
                                 fullname=driver.fullname,
                                 team=driver.team,
                                 time=driver.best_lap) for driver in rows]
        with db.atomic():
            for driver in create_info:
                try:
                    driver.save()
                    logging.info(f"Created row with id: {driver} and driver_id: {driver.abbr}")
                except IntegrityError:
                    logging.warning(f"Skipping duplicate entry with driver_id: {driver.abbr}")
                    continue
