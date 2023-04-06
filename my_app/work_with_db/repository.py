from .models import DriverModel


class DriversRepository:
    model = DriverModel

    def get(self) -> list[DriverModel]:
        return self.model.select()

    def get_single(self, abbr: str) -> DriverModel | None:
        return self.model.get_or_none(DriverModel.abbr == abbr)
