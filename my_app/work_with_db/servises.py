from my_app.work_with_db.models import DriverModel
from my_app.work_with_db.repository import DriverRepository, DriversRepository


def get_drivers_query() -> list[DriverModel]:
    repository = DriversRepository()
    return repository.get()


def get_single_driver(abbr: str) -> DriverModel:
    repository = DriverRepository()
    return repository.get(abbr)
