from flasgger import swag_from
from flask import Response, jsonify, make_response, request
from flask_restful import Resource

from my_app.functions_view import HandleMyData, format_check
from my_app.servises import get_drivers_query, get_single_driver


class Report(Resource):
    @swag_from('swagger/report.yml')
    def get(self) -> Response:
        query = sorted(get_drivers_query(), key=lambda x: x.time)
        handle = HandleMyData()
        args = request.args.to_dict()

        racers_list = handle.racers_add_place(handle.racers_list_of_full_dict(query))

        return format_check(args.get("format"), racers_list, 200)


class Drivers(Resource):
    @swag_from('swagger/drivers.yml')
    def get(self) -> Response:
        query = get_drivers_query()
        handle = HandleMyData()
        args = request.args

        racers_list_of_dict = handle.racers_list_of_small_dict(query)

        return format_check(args.get("format"), racers_list_of_dict, 200)


class Driver(Resource):
    @swag_from("swagger/driver.yml")
    def get(self, driver_id: str) -> Response:
        handle = HandleMyData()
        args = request.args.to_dict()
        driver_id = driver_id.strip().upper()
        driver = get_single_driver(driver_id)

        if driver:
            driver_dict = handle.racer_to_full_dict(driver)

            return format_check(args.get("format"), driver_dict, 200)

        return make_response(jsonify("Driver not found"), 404)
