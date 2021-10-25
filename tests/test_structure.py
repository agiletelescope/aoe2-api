import pytest

from aoe2_api.shared.config import *
from aoe2_api.models.cost import Cost
from aoe2_api.models.age import Age
from aoe2_api.models.structure import Structure

# Helpers
_valid_cost = Cost(1)
_valid_age = Age.DARK


@pytest.mark.parametrize(
    "name, age, cost, build_time_sec, hit_points, expected_return",
    [
        # Name
        (None, _valid_age, _valid_cost, 1, 1, False),
        ([], _valid_age, _valid_cost, 1, 1, False),
        ({}, _valid_age, _valid_cost, 1, 1, False),
        (True, _valid_age, _valid_cost, 1, 1, False),
        (1, _valid_age, _valid_cost, 1, 1, False),
        ("", _valid_age, _valid_cost, 1, 1, False),
        ("a" * (MAX_VALUE_LIMIT + 1), _valid_age, _valid_cost, 1, 1, False),
        ("a" * MAX_VALUE_LIMIT, _valid_age, _valid_cost, 1, 1, True),
        ("valid_name", _valid_age, _valid_cost, 1, 1, True),

        # Age
        ("name", None, _valid_cost, 1, 1, False),
        ("name", [], _valid_cost, 1, 1, False),
        ("name", {}, _valid_cost, 1, 1, False),
        ("name", "age", _valid_cost, 1, 1, False),
        ("name", True, _valid_cost, 1, 1, False),
        ("name", 1, _valid_cost, 1, 1, False),
        ("name", Age.IMPERIAL, _valid_cost, 1, 1, True),

        # Cost
        ("name", _valid_age, None, 1, 1, False),
        ("name", _valid_age, [], 1, 1, False),
        ("name", _valid_age, {}, 1, 1, False),
        ("name", _valid_age, "cost", 1, 1, False),
        ("name", _valid_age, True, 1, 1, False),
        ("name", _valid_age, 1, 1, 1, False),
        ("name", _valid_age, Cost(), 1, 1, False),
        ("name", _valid_age, Cost(1, 2, 3, 4), 1, 1, True),

        # Build Time
        ("name", _valid_age, _valid_cost, None, 1, False),
        ("name", _valid_age, _valid_cost, [], 1, False),
        ("name", _valid_age, _valid_cost, {}, 1, False),
        ("name", _valid_age, _valid_cost, "time", 1, False),
        ("name", _valid_age, _valid_cost, True, 1, False),
        # Can't be negative
        ("name", _valid_age, _valid_cost, -1, 1, False),
        ("name", _valid_age, _valid_cost, 2*MAX_VALUE_LIMIT, 1, False),
        ("name", _valid_age, _valid_cost, -2*MAX_VALUE_LIMIT, 1, False),
        ("name", _valid_age, _valid_cost, MAX_VALUE_LIMIT, 1, True),
        # 0 is a valid value
        ("name", _valid_age, _valid_cost, 0, 1, True),
        ("name", _valid_age, _valid_cost, MAX_VALUE_LIMIT - 1, 1, True),

        # Hit points
        ("name", _valid_age, _valid_cost, 1, None, False),
        ("name", _valid_age, _valid_cost, 1, [], False),
        ("name", _valid_age, _valid_cost, 1, {}, False),
        ("name", _valid_age, _valid_cost, 1, "hp", False),
        ("name", _valid_age, _valid_cost, 1, True, False),
        # Unit health can't be 0
        ("name", _valid_age, _valid_cost, 1, 0, False),
        ("name", _valid_age, _valid_cost, 1, -1, False),
        ("name", _valid_age, _valid_cost, 1, 2*MAX_VALUE_LIMIT, False),
        ("name", _valid_age, _valid_cost, 1, -2 * MAX_VALUE_LIMIT, False),

        # Random
        (1, 2, 3, 4, 5, False),
        ("", Age.DARK, Cost(food=1), 10, 10, False),
        ("name", Age.DARK, Cost(), 10, 10, False),
        ("name", Age.DARK, Cost(food=1), -1, 10, False),
        ("name", Age.DARK, Cost(wood=MAX_VALUE_LIMIT+1), 10, 10, False),
        ("a" * (MAX_VALUE_LIMIT + 1), Age.DARK, Cost(gold=1), 1, 1, False),
        ("name", _valid_age, _valid_cost, 1, 1, True),
        ("name", Age.CASTLE, Cost(wood=1), 1, MAX_VALUE_LIMIT, True),
    ]
)
def test_structure_validity(name: str, age: Age, cost: Cost,
                            build_time_sec: int, hit_points: int,
                            expected_return: bool):
    s = Structure(name, age, cost, build_time_sec, hit_points)
    ret = s.is_valid()

    assert isinstance(ret, bool)
    assert ret == expected_return


@pytest.mark.parametrize(
    # "," is assumed to be the separator
    "value, expected_output",
    [
        # 1. Invalid types
        (None, None),
        ([], None),
        (True, None),
        (1, None),
        ({}, None),

        # 2. Bad values
        ("", None),
        ("abcd", None),
        ("1,2,3,4,5,6", None),
        ("a,b,"*10, None),
        ("name, [], [], {}, 100, aa", None),
        ('name, Dark, {"Gold": 1}, 1, None', None),
        ('name, Dark, {"Gold": 1}, None, 0', None),
        ('name, Dark, None, 100, 10', None),
        ('name, 0, {"Gold": 1}, 100, 10', None),
        # Name too large
        ("aa"*MAX_VALUE_LIMIT + ', Dark, {"Gold": 1}, 100, 10', None),
        (',, 0, {"Gold": 1}, 100, 10', None),
        ('name, dark, {"Food": 1}, 1, 0', None),
        ('name, dark, {"Food": 1}, ' + str(MAX_VALUE_LIMIT + 1) + ', 10', None),
        ('name, dark, {"Food": 1}, 10, ' + str(MAX_VALUE_LIMIT + 1), None),
        # Parse err, values and resources both split by ,
        ('name, Feudal, {"Gold": 1, "Food": 2}, 100, 10', None),

        # 3. Valid cases
        ('name,dark,{"Food": 1},1,1',
         Structure("name", Age.DARK, Cost(food=1), 1, 1)),
        ('name, dark, {"Food": 1}, 1, 1',                       # leading space before ,
         Structure("name", Age.DARK, Cost(food=1), 1, 1)),
        ('name, dark, {"Food": 1}, 0, 1',                       # Build time can be 0
         Structure("name", Age.DARK, Cost(food=1), 0, 1)),
        ('[], CASTLE, {"Gold": 1}, 100, 10',                    # "[]" is a valid name
         Structure("[]", Age.CASTLE, Cost(gold=1), 100, 10)),
        ('name, CASTLE, {"Gold": 1; "Food": 2}, 100, 10',
         Structure("name", Age.CASTLE, Cost(gold=1, food=2), 100, 10)),
    ]
)
def test_structure_parse(value: str, expected_output: Structure):
    ret = Structure.from_str(value)
    assert isinstance(ret, Structure) or ret is None
    assert ret == expected_output
