import pytest

from aoe2_api.shared.config import *
from aoe2_api.models.cost import Cost
from aoe2_api.models.age import Age
from aoe2_api.models.unit import Unit

# Helpers
_valid_cost = Cost(1)
_invalid_cost = Cost()
_valid_age = Age.DARK
_valid_desc = "description"
_valid_ci = "Barracks"


@pytest.mark.parametrize(
    "name, age, cost, description, created_in, expected_return",
    [
        # Name
        (None, _valid_age, _valid_cost, _valid_desc, _valid_ci, False),
        ([], _valid_age, _valid_cost, _valid_desc, _valid_ci, False),
        ({}, _valid_age, _valid_cost, _valid_desc, _valid_ci, False),
        (True, _valid_age, _valid_cost, _valid_desc, _valid_ci, False),
        (1, _valid_age, _valid_cost, _valid_desc, _valid_ci, False),
        ("", _valid_age, _valid_cost, _valid_desc, _valid_ci, False),
        ("a" * (MAX_VALUE_LIMIT + 1), _valid_age, _valid_cost, _valid_desc, _valid_ci, False),
        ("a" * MAX_VALUE_LIMIT, _valid_age, _valid_cost, _valid_desc, _valid_ci, True),

        # Age
        ("name", None, _valid_cost, _valid_desc, _valid_ci, False),
        ("name", [], _valid_cost, _valid_desc, _valid_ci, False),
        ("name", {}, _valid_cost, _valid_desc, _valid_ci, False),
        ("name", "age", _valid_cost, _valid_desc, _valid_ci, False),
        ("name", True, _valid_cost, _valid_desc, _valid_ci, False),
        ("name", 1, _valid_cost, _valid_desc, _valid_ci, False),

        # Cost
        ("name", _valid_age, None, _valid_desc, _valid_ci, False),
        ("name", _valid_age, [], _valid_desc, _valid_ci, False),
        ("name", _valid_age, {}, _valid_desc, _valid_ci, False),
        ("name", _valid_age, "cost", _valid_desc, _valid_ci, False),
        ("name", _valid_age, True, _valid_desc, _valid_ci, False),
        ("name", _valid_age, 1, _valid_desc, _valid_ci, False),
        ("name", _valid_age, Cost(), _valid_desc, _valid_ci, False),

        # Description
        ("name", _valid_age, _valid_cost, None, _valid_ci, False),
        ("name", _valid_age, _valid_cost, [], _valid_ci, False),
        ("name", _valid_age, _valid_cost, {}, _valid_ci, False),
        ("name", _valid_age, _valid_cost, True, _valid_ci, False),
        ("name", _valid_age, _valid_cost, "", _valid_ci, False),
        ("name", _valid_age, _valid_cost, "a" * (MAX_VALUE_LIMIT + 1), _valid_ci, False),
        ("name", _valid_age, _valid_cost, "a" * MAX_VALUE_LIMIT, _valid_ci, True),

        # Created In
        ("name", _valid_age, _valid_cost, _valid_desc, None, False),
        ("name", _valid_age, _valid_cost, _valid_desc, [], False),
        ("name", _valid_age, _valid_cost, _valid_desc, {}, False),
        ("name", _valid_age, _valid_cost, _valid_desc, True, False),
        ("name", _valid_age, _valid_cost, _valid_desc, "", False),
        ("name", _valid_age, _valid_cost, _valid_desc, "a" * (MAX_VALUE_LIMIT + 1), False),
        ("name", _valid_age, _valid_cost, _valid_desc, "a" * MAX_VALUE_LIMIT, True),
        ("name", _valid_age, _valid_cost, _valid_desc, "created in", True),

        # Random
        (1, 2, 3, 4, 5, False),
        ("name", None, Cost(), "des", "cre", False),
        ("name", [], None, "des", "cre", False),
        ("name", Age.FEUDAL, Cost(wood=1), 1, "cre", False),
        ("name", Age.DARK, Cost(gold=1), "des", {}, False),
        ("name", Age.CASTLE, Cost(), "d", "c", False),
        ("name", Age.FEUDAL, Cost(gold=1), "d" * (MAX_VALUE_LIMIT + 1), "c", False),
        ("name", Age.FEUDAL, Cost(gold=1), "d", "c" * (MAX_VALUE_LIMIT + 1), False),
        ("name", Age.DARK, Cost(gold=1), "desc", "cre", True),
        ("[]-9921", Age.DARK, Cost(gold=1), "desc", "cre", True),
        ("valid_name", _valid_age, _valid_cost, _valid_desc, _valid_ci, True),
        ("name", Age.CASTLE, Cost(gold=1), "d" * MAX_VALUE_LIMIT, "c", True),
    ]
)
def test_unit_validity(name: str, age: Age, cost: Cost,
                       description: str, created_in: str, expected_return: bool):
    s = Unit(name, age, cost, description, created_in)
    ret = s.is_valid()

    assert isinstance(ret, bool)
    assert ret == expected_return


@pytest.mark.parametrize(
    "value, expected_output",
    [
        # Invalid types
        (None, None),
        ([], None),
        (True, None),
        (1, None),
        ({}, None),

        # Bad values
        ("", None),
        ("abcd", None),
        ("1,2,3,4,5,6", None),
        ("a,b," * 10, None),
        ("name, [], [], {}, 100, aa", None),
        ('name, 0, {"Gold": 1}, 100, 10', None),
        ("aa" * MAX_VALUE_LIMIT + ', Dark, {"Gold": 1}, 100, 10', None),
        (',, 0, {"Gold": 1}, 100, 10', None),
        ('name, dark, {"Food": 1}, ' + "a" * (MAX_VALUE_LIMIT + 1) + ', 10', None),
        ('name, dark, {"Food": 1}, 10, ' + "a" * (MAX_VALUE_LIMIT + 1), None),
        # Parse err, values and resources both split by ,
        ('name, Feudal, {"Gold": 1, "Food": 2}, aa, bb', None),
        ('name, Feudal, {"Gold": 1; "Food": 2}, aa, bb, cc, dd', None),
        # Description or created_in empty
        ('name, dark, {"Food": 1}, , b', None),
        ('name, dark, {"Food": 1}, s, ', None),

        # Valid cases
        ('name,dark,{"Food": 1},a,b',
         Unit("name", Age.DARK, Cost(food=1), "a", "b")),
        ('name, dark, {"Food": 1}, a, b',  # leading space before ,
         Unit("name", Age.DARK, Cost(food=1), "a", "b")),
        ('name, dark, {"Food": 1}, a, b',  # Build time can be 0
         Unit("name", Age.DARK, Cost(food=1), "a", "b")),
        ('[], CASTLE, {"Gold": 1}, a, b',  # "[]" is a valid name
         Unit("[]", Age.CASTLE, Cost(gold=1), "a", "b")),
        ('name, CASTLE, {"Gold": 1; "Food": 2}, abcde, xyz',
         Unit("name", Age.CASTLE, Cost(gold=1, food=2), "abcde", "xyz")),
        ('name, Dark, {"Gold": 1}, None, None',
         Unit("name", Age.DARK, Cost(gold=1), "None", "None")),
        ('name, Imperial, {"Gold": 1}, asdf, 1000',
         Unit("name", Age.IMPERIAL, Cost(gold=1), "asdf", "1000")),
        ('name, Feudal, {"Gold": 1; "Food": 2}, aa, bb',
         Unit("name", Age.FEUDAL, Cost(gold=1, food=2), "aa", "bb")),
    ]
)
def test_unit_parser(value: str, expected_output: Unit):
    ret = Unit.from_str(value)
    assert isinstance(ret, Unit) or ret is None
    assert ret == expected_output
