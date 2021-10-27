import pytest

from aoe2_api.shared.config import *
from aoe2_api.models.cost import Cost
from aoe2_api.services.datastore import DataStore

from tests.conftest import mock_units
from tests.conftest import mock_structures


@pytest.mark.parametrize(
    "cost, expected_output",
    [
        # Invalid types
        (None, []),
        (1, []),
        (True, []),
        ([], []),
        ({}, []),
        ("", []),

        # Invalid data
        (Cost(), []),
        (Cost(gold=-1), []),

        # Valid cases
        (Cost(wood=10), []),
        (Cost(wood=200), [mock_structures[0]]),
        (Cost(stone=1), []),
        (Cost(stone=150), [mock_structures[1]]),
        (Cost(gold=1), []),
        (Cost(gold=59), []),
        (Cost(gold=70), [mock_structures[2]]),
        (Cost(gold=20, wood=30, food=60), [mock_structures[3]]),
        (Cost(gold=60, wood=10, food=60, stone=10), mock_structures[2:5]),
    ]
)
def test_filter_structures(cost: Cost, expected_output: list):
    datastore = DataStore(
        MOCK_STRUCTURES_FILE_PATH,
        MOCK_UNITS_DATA_FILE_PATH)
    assert isinstance(datastore, DataStore)

    ret = datastore.filter_structures(cost)
    assert type(ret) == list
    assert ret == expected_output


@pytest.mark.parametrize(
    "cost, expected_output",
    [
        # Invalid types
        (None, []),
        (1, []),
        (True, []),
        ([], []),
        ({}, []),
        ("", []),

        # Invalid data
        (Cost(), []),
        (Cost(gold=-1), []),

        # Valid cases
        (Cost(wood=1), []),
        (Cost(wood=10), [mock_units[0]]),
        (Cost(wood=25, gold=50), [
            mock_units[0],
            mock_units[1],
            mock_units[3],
            mock_units[4],
        ]),
        (Cost(wood=25, gold=45, stone=10), mock_units),
        (Cost(gold=20, wood=30, food=60), [mock_units[0]]),
        (Cost(gold=60, wood=10, food=60, stone=10), [mock_units[0]]),
    ]
)
def test_filter_units(cost: Cost, expected_output: list):
    datastore = DataStore(
        MOCK_STRUCTURES_FILE_PATH,
        MOCK_UNITS_DATA_FILE_PATH)
    assert isinstance(datastore, DataStore)

    ret = datastore.filter_units(cost)
    assert type(ret) == list
    assert ret == expected_output
