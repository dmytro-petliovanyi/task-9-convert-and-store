import xml.etree.ElementTree as Et
from unittest.mock import patch

from test_my_app.conftest import (drivers_query_for_tests,
                                  full_list_of_dict_for_test,
                                  full_list_of_dict_for_test_with_place,
                                  full_list_of_dict_for_test_with_place_desc,
                                  small_list_of_dict_for_test)


@patch("my_app.resources.DriversRepository.get", return_value=drivers_query_for_tests)
def test_report_default_route(patch_drivers_query, client):
    response = client.get("/api/v1/report/")
    patch_drivers_query.assert_called()
    assert response.status_code == 200
    for racer in full_list_of_dict_for_test_with_place:
        assert racer in response.json


@patch("my_app.resources.DriversRepository.get", return_value=drivers_query_for_tests)
def test_report_desc_route(patch_drivers_query, client):
    response = client.get("/api/v1/report/?order=desc")
    patch_drivers_query.assert_called()
    assert response.status_code == 200
    for racer in full_list_of_dict_for_test_with_place_desc:
        assert racer in response.json


@patch("my_app.resources.DriversRepository.get", return_value=drivers_query_for_tests)
def test_report_asc_route(patch_drivers_query, client):
    response = client.get("/api/v1/report/?order=asc")
    patch_drivers_query.assert_called()
    assert response.status_code == 200
    for racer in full_list_of_dict_for_test_with_place:
        assert racer in response.json


@patch("my_app.resources.DriversRepository.get", return_value=drivers_query_for_tests)
def test_report_json_route(patch_drivers_query, client):
    response = client.get("/api/v1/report/?format=json")
    patch_drivers_query.assert_called()
    assert response.status_code == 200
    for racer in full_list_of_dict_for_test_with_place:
        assert racer in response.json


@patch("my_app.resources.DriversRepository.get", return_value=drivers_query_for_tests)
def test_report_xml_route(patch_drivers_query, client):
    response = client.get("/api/v1/report/?format=xml")
    patch_drivers_query.assert_called()
    assert response.status_code == 200

    root = Et.fromstring(response.data)
    items = root.findall("item")
    for index in range(len(items)):
        item = items[index]
        racer_dict = full_list_of_dict_for_test_with_place[index]
        assert item.find("abbr").text == racer_dict["abbr"]
        assert item.find("fullname").text == racer_dict["fullname"]
        assert item.find("place").text == str(racer_dict["place"])
        assert item.find("team").text == racer_dict["team"]
        assert item.find("time").text == racer_dict["time"]


@patch("my_app.resources.DriversRepository.get", return_value=drivers_query_for_tests)
def test_drivers_default_route(patch_drivers_query, client):
    response = client.get("/api/v1/report/drivers/")
    patch_drivers_query.assert_called()
    assert response.status_code == 200
    for racer in small_list_of_dict_for_test:
        assert racer in response.json


@patch("my_app.resources.DriversRepository.get", return_value=drivers_query_for_tests)
def test_drivers_xml_route(patch_drivers_query, client):
    response = client.get("/api/v1/report/drivers/?format=xml")
    patch_drivers_query.assert_called()
    assert response.status_code == 200

    root = Et.fromstring(response.data)
    items = root.findall("item")
    for index in range(len(items)):
        item = items[index]
        racer_dict = small_list_of_dict_for_test[index]
        assert item.find("abbr").text == racer_dict["abbr"]
        assert item.find("fullname").text == racer_dict["fullname"]


@patch("my_app.resources.DriversRepository.get_single", return_value=drivers_query_for_tests[0])
def test_driver_default_route(patch_single_driver, client):
    response = client.get("/api/v1/report/drivers/DRR/")
    patch_single_driver.assert_called()
    assert response.status_code == 200
    assert full_list_of_dict_for_test[0] == response.json


@patch("my_app.resources.DriversRepository.get_single", return_value=drivers_query_for_tests[0])
def test_driver_xml_route(patch_single_driver, client):
    response = client.get("/api/v1/report/drivers/DRR/?format=xml")
    patch_single_driver.assert_called()
    assert response.status_code == 200

    root = Et.fromstring(response.data)
    racer_dict = full_list_of_dict_for_test[0]
    assert root.find("abbr").text == racer_dict["abbr"]
    assert root.find("fullname").text == racer_dict["fullname"]
    assert root.find("team").text == racer_dict["team"]
    assert root.find("time").text == racer_dict["time"]


@patch("my_app.resources.DriversRepository.get_single", return_value=None)
def test_driver_not_found(patch_single_driver, client):
    response = client.get("/api/v1/report/drivers/SGV/")
    patch_single_driver.assert_called()
    assert response.status_code == 404
    assert 'Driver not found' == response.json
