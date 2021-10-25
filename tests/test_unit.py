import pytest

from aoe2_api.shared.config import *
from aoe2_api.models.cost import Cost
from aoe2_api.models.age import Age
from aoe2_api.models.unit import Unit


@pytest.mark.parametrize(
    "name, age, cost, description, created_in, expected_return",
    [
        # 1. Bad data types
        (1, 2, 3, 4, 5, False),
        ("name", None, Cost(), "des", "cre", False),
        ("name", [], None, "des", "cre", False),
        ("name", Age.FEUDAL, Cost(wood=1), 1, "cre", False),
        ("name", Age.DARK, Cost(gold=1), "des", {}, False),

        # 2. Bad values
        ("", Age.DARK, Cost(food=1), "d", "c", False),  # Empty name
        ("name", Age.DARK, Cost(food=1), "", "c", False),  # Empty description
        ("name", Age.DARK, Cost(food=1), "d", "", False),  # Empty created_in
        ("name", Age.CASTLE, Cost(), "d", "c", False),
        ("name", Age.FEUDAL, Cost(gold=1), "d" * (MAX_VALUE_LIMIT + 1), "c", False),
        ("name", Age.FEUDAL, Cost(gold=1), "d", "c" * (MAX_VALUE_LIMIT + 1), False),

        # 3. Valid cases
        ("name", Age.DARK, Cost(gold=1), "desc", "cre", True),
        ("[]-9921", Age.DARK, Cost(gold=1), "desc", "cre", True),
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
        # 1. Invalid types
        (None, None),
        ([], None),
        (True, None),
        (1, None),
        ({}, None),

        # 2. Bad values
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
        ('name, dark, {"Food": 1}, , b', None),
        ('name, dark, {"Food": 1}, s, ', None),

        # 3. Valid cases
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
    ]
)
def test_unit_parser(value: str, expected_output: Unit):
    ret = Unit.from_str(value)
    assert isinstance(ret, Unit) or ret is None
    assert ret == expected_output
