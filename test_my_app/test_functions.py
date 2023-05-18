from unittest.mock import patch

from my_app.functions_view import HandleMyData, get_abbr
from test_my_app.conftest import (drivers_query_for_tests,
                                  full_list_of_dict_for_test,
                                  full_list_of_dict_for_test_with_place,
                                  full_list_of_dict_for_test_with_place_desc,
                                  racers_for_patch,
                                  small_list_of_dict_for_test)


@patch("my_app.functions_view.HandleMyData.racer_to_full_dict", side_effect=full_list_of_dict_for_test)
def test_racers_list_of_full_dict_works_as_expected(patch_racer_to_full_dict):
    handle = HandleMyData()
    result = handle.racers_list_of_full_dict(racers_for_patch)
    patch_racer_to_full_dict.assert_called()
    assert result == full_list_of_dict_for_test


@patch("my_app.functions_view.HandleMyData.racer_to_small_dict", side_effect=small_list_of_dict_for_test)
def test_racers_list_of_small_dict_works_as_expected(patch_racer_to_small_dict):
    handle = HandleMyData()
    result = handle.racers_list_of_small_dict(racers_for_patch)
    patch_racer_to_small_dict.assert_called()
    assert result == small_list_of_dict_for_test


def test_racer_to_full_dict():
    handle = HandleMyData()
    result = handle.racer_to_full_dict(drivers_query_for_tests[0])
    assert result == full_list_of_dict_for_test[0]


def test_racer_to_small_dict():
    handle = HandleMyData()
    result = handle.racer_to_small_dict(drivers_query_for_tests[0])
    assert result == small_list_of_dict_for_test[0]


@patch("my_app.functions_view.HandleMyData.add_place", side_effect=full_list_of_dict_for_test_with_place)
def test_racers_add_place(patch_add_place):
    handle = HandleMyData()
    result = handle.racers_add_place(full_list_of_dict_for_test)
    patch_add_place.assert_called()
    assert full_list_of_dict_for_test_with_place == result


def test_add_place():
    handle = HandleMyData()
    result = handle.add_place(full_list_of_dict_for_test[2], 1)
    assert result == full_list_of_dict_for_test_with_place_desc[0]


def test_get_abbr_works_as_expected():
    result = [get_abbr(racer) for racer in racers_for_patch]
    assert result == ["DRR", "SVF", "LHM"]
