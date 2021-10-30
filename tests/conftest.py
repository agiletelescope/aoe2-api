import os
import sys
import pytest

# Make server accessible for tests
api_dir = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.insert(0, api_dir)

from aoe2_api.models.age import Age
from aoe2_api.models.cost import Cost
from aoe2_api.models.unit import Unit
from aoe2_api.models.structure import Structure
from aoe2_api.app import create_app

"""
Pytest Config file,
Houses all initializations and fixtures

Pytest Docs - https://docs.pytest.org/en/6.2.x/
Pytest Fixtures - https://docs.pytest.org/en/6.2.x/fixture.html
Pytest Parameterized testing - https://docs.pytest.org/en/6.2.x/example/parametrize.html
Flask Testing Docs - https://flask.palletsprojects.com/en/2.0.x/testing/

pytest -v (verbose) -s (show print statements)
"""


# Mock Data
mock_structures = [
    Structure("a", Age.DARK, Cost(wood=175), 50, 1200),
    Structure("b", Age.FEUDAL, Cost(stone=150), 35, 1800),
    Structure("c", Age.CASTLE, Cost(gold=60), 15, 480),
    Structure("d", Age.DARK, Cost(food=60), 5, 48),
    Structure("e", Age.IMPERIAL, Cost(food=60, wood=10, gold=1, stone=9), 50, 800),
    Structure("i", Age.CASTLE, Cost(gold=10, food=20), 34, 499),
    Structure("j", Age.FEUDAL, Cost(stone=30, wood=77), 12, 21),
    Structure("k", Age.IMPERIAL, Cost(food=1, wood=24), 201, 38),
]
mock_units = [
    Unit("a", Age.FEUDAL, Cost(wood=2), "desc1", "building1"),
    Unit("b", Age.IMPERIAL, Cost(wood=25, gold=45), "desc2", "building2"),
    Unit("c", Age.CASTLE, Cost(wood=25, gold=45, stone=10), "desc3", "building2"),
    Unit("d", Age.FEUDAL, Cost(wood=25, gold=45), "desc4", "building2"),
    Unit("e", Age.DARK, Cost(wood=25, gold=45), "desc5", "building1"),
]


@pytest.fixture
def app():
    flask_app, _ = create_app(is_testing=True)
    # If create_app fails, the tests fail
    # Hence the return code from create_app can be ignored

    return flask_app.test_client()


@pytest.fixture
def structures_data():
    return mock_structures


@pytest.fixture
def units_data():
    return mock_units
