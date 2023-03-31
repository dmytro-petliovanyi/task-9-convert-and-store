from xml.dom.minidom import parseString

from dicttoxml import dicttoxml
from flask import Response, jsonify, make_response
from report_of_monaco_racing import Racer

from my_app.models import DriverModel
from my_app.my_settings.constants import FormatEnum


class HandleMyData:
    def __init__(self, query: list[DriverModel]) -> None:
        self._drivers_data = query

    def racers_list_of_full_dict(self) -> list[dict]:
        return [self.racer_to_full_dict(racer) for racer in self._drivers_data]

    def racers_list_of_small_dict(self) -> list[dict]:
        return [self.racer_to_small_dict(racer) for racer in self._drivers_data]

    def find_racer(self, driver_id: str) -> DriverModel | None:
        for driver in self._drivers_data:
            if driver.abbr == driver_id:
                return driver

    def racers_add_place(self, racers_list_of_dict: list[dict]) -> list[dict]:
        for index in range(0, len(racers_list_of_dict)):
            racers_list_of_dict[index] = self.add_place(racers_list_of_dict[index], index + 1)
        return racers_list_of_dict

    @staticmethod
    def add_place(racer_dict: dict, place) -> dict:
        racer_dict["place"] = place
        return racer_dict

    @staticmethod
    def racer_to_full_dict(racer: DriverModel) -> dict:
        return {"abbr": racer.abbr,
                "fullname": racer.fullname,
                "team": racer.team,
                "time": str(racer.time)}

    @staticmethod
    def racer_to_small_dict(racer: DriverModel) -> dict:
        return {"abbr": racer.abbr,
                "fullname": racer.fullname}


def get_abbr(driver: Racer) -> str:
    name_split = driver.fullname.split()
    driver_abbr = name_split[0][0] + name_split[1][0] + driver.team[0]
    return driver_abbr


def format_handle(racers_list_or_dict: list[dict] | dict, form: str | None) -> Response | str:
    if form:
        form = FormatEnum(form)

        if form == FormatEnum.xml:
            xml = dicttoxml(racers_list_or_dict, attr_type=False)
            dom = parseString(xml)

            return dom.toprettyxml()

    return jsonify(racers_list_or_dict)


def format_check(form: str | None, racers_list_or_dict: list[dict] | dict, code: int) -> Response:
    data = format_handle(racers_list_or_dict, form)

    return make_response(data, code)
