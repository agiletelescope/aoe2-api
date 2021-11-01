import pytest

from aoe2_api.shared.statuscodes import *
from aoe2_api.models.cost import Cost
from aoe2_api.shared.utils import remove_none_keys

from tests.conftest import mock_units


"""
Tests for structures blueprint,
Located at aoe2_api/routes/units/routes.py
"""


@pytest.mark.parametrize(
    "gold, food, wood, stone, response_data, http_code, return_code",
    [
        # Gold
        (None, 1, 1, 1, [], 201, SUCCESS),
        ({}, 1, 1, 1, [], 400, INVALID_DATA_FORMAT),
        ("invalid", 1, 1, 1, [], 400, INVALID_DATA_FORMAT),
        (61, 1, 1, 1, [mock_units[8].to_json()], 201, SUCCESS),

        # Food
        (1, None, 1, 1, [mock_units[8].to_json()], 201, SUCCESS),
        (1, {}, 1, 1, [], 400, INVALID_DATA_FORMAT),
        (1, "invalid", 1, 1, [], 400, INVALID_DATA_FORMAT),
        (1, 65, 1, 1, [mock_units[8].to_json()], 201, SUCCESS),

        # Wood
        (1, 1, None, 1, [mock_units[8].to_json()], 201, SUCCESS),
        (1, 1, {}, 1, [], 400, INVALID_DATA_FORMAT),
        (1, 1, "invalid", 1, [], 400, INVALID_DATA_FORMAT),
        (0, 1, 180, 1, [mock_units[0].to_json()], 201, SUCCESS),

        # Stone
        (0, 1, 1, None, [], 201, SUCCESS),
        (0, 1, 1, {}, [], 400, INVALID_DATA_FORMAT),
        (0, 1, 1, "invalid", [], 400, INVALID_DATA_FORMAT),
        (1, 1, 1, 10, [i.to_json() for i in mock_units[-2:]], 201, SUCCESS),

        # Random
        (None, None, None, None, [], 400, INVALID_DATA_FORMAT),
        (1, 60, 25, 100, [
            mock_units[i].to_json() for i in [0, 5, 8, 9]
        ], 201, SUCCESS),
        (100, 100, 100, 100, [
            mock_units[i].to_json() for i in [0, 1, 2, 3, 4, 5, 7, 8, 9]
        ], 201, SUCCESS),
    ]
)
def test_get_units(app, units_data, gold, food, wood, stone,
                   response_data, http_code, return_code):

    body = dict(gold=gold, food=food, wood=wood, stone=stone)
    request = app.post('/units/', json=remove_none_keys(body))

    assert request is not None
    assert request.get_json() is not None

    request_return_code = request.get_json().get('code') or 0
    assert request_return_code == return_code
    assert request.status_code == http_code

    if request.status_code != 201:
        return

    cost = Cost(gold=gold, food=food, wood=wood, stone=stone)
    expected_data = [s.to_json() for s in units_data
                     if s.can_create(cost)]
    assert 'data' in request.get_json()
    assert request.get_json()["data"] == expected_data
    assert request.get_json()["data"] == response_data
