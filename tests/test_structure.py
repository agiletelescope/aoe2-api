import pytest

from aoe2_api.shared.config import *
from aoe2_api.models.cost import Cost
from aoe2_api.models.age import Age
from aoe2_api.models.structure import Structure


@pytest.mark.parametrize(
    "name, age, cost, build_time_sec, hit_points, expected_return",
    [
        # 1. Bad data types
        (1, 2, 3, 4, 5, False),
        ("name1", None, Cost(wood=1), 10, 10, False),
        ("name1", True, Cost(wood=1), 10, 10, False),
        ("name2", [], Cost(stone=1), 10, 10, False),
        ("name3", Age.DARK, {}, 10, 10, False),
        ("name4", Age.IMPERIAL, Cost(food=1), "abcd", 10, False),
        ("name5", Age.FEUDAL, Cost(gold=1), None, [], False),

        # 2. Bad values
        ("", Age.DARK, Cost(food=1), 10, 10, False),        # Empty name
        ("name", Age.DARK, Cost(), 10, 10, False),          # Empty cost
        ("name", Age.DARK, Cost(food=1), 10, 0, False),     # Hit points can't be 0
        ("name", Age.DARK, Cost(food=1), -1, 10, False),    # Hit points can't be negative
        ("name", Age.DARK, Cost(food=1), 1, -100, False),   # Build time can't be negative
        ("name", Age.DARK, Cost(wood=MAX_VALUE_LIMIT+1),
         10, 10, False),                                    # Resources too high
        ("name", Age.DARK,
         Cost(gold=MAX_VALUE_LIMIT+1), 10, 10, False),      # gold > max limit
        ("name", Age.DARK, Cost(gold=1), 10, 0, False),     # hit_points < 1
        ("a" * (MAX_VALUE_LIMIT + 1),
         Age.DARK, Cost(gold=1), 1, 1, False),              # Name too large

        # 3. Valid cases
        ("name", Age.DARK, Cost(gold=1), 1, 1, True),
        ("name", Age.DARK, Cost(food=1), 0, 10, True),      # Build time can be 0
        ("name", Age.CASTLE, Cost(wood=1), MAX_VALUE_LIMIT, 10, True),
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
