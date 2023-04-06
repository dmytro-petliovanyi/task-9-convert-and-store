from my_app.work_with_db.models import DriverModel


class DriversRepository:
    model = DriverModel

    def get(self) -> list[DriverModel]:
        return self.model.select()

    def get_single(self, abbr: str) -> DriverModel:
        return self.model.get(DriverModel.abbr == abbr)
