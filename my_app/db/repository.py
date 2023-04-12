from peewee import IntegrityError

from logging_config import logging

from .models import DriverModel, db


class DriversRepository:
    model = DriverModel

    def get(self) -> list[DriverModel]:
        return self.model.select()

    def get_single(self, abbr: str) -> DriverModel | None:
        return self.model.get_or_none(DriverModel.abbr == abbr)

    def create_from_list(self, rows: list[dict]):
        create_info = [self.model(id=rows.index(driver)+1,
                                  abbr=driver["abbr"],
                                  fullname=driver["fullname"],
                                  team=driver["team"],
                                  time=driver["time"]) for driver in rows]
        with db.atomic():
            for driver in create_info:
                try:
                    driver.save()
                    logging.info(f"Created row with id: {driver} and driver_id: {driver.abbr}")
                except IntegrityError:
                    logging.warning(f"Skipping duplicate entry with driver_id: {driver.abbr}")
                    continue
