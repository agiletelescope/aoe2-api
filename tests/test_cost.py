import pytest

from aoe2_api.shared.config import *
from aoe2_api.models.cost import Cost


@pytest.mark.parametrize(
    "gold, food, wood, stone, expected_return",
    [
        # 1. Bad data types
        ("a", 0, 0, 0, False),
        (0, [], 0, 0, False),
        (0, 0, {}, 0, False),
        (0, 0, 0, Cost(), False),
        (0, 0, True, 0, False),
        ("a", [], True, Cost(), False),

        # 2. None types
        (0, None, None, None, True),
        (None, None, None, None, True),

        # 3. Bad values
        (-1, -1929, 0, 0, False),                      # Gold value < 0
        (0, MAX_VALUE_LIMIT + 1, 0, 0, False),      # Food value > limit
        (0.21, 9.32, 88, 91, False),                   # Decimal values

        # 4. Valid cases
        (0, 0, 0, 0, True),
        (10, 20, 88, 91, True),
        (1000, 0, MAX_VALUE_LIMIT - 1, 0, True),
        (10, 20, MAX_VALUE_LIMIT, 91, True),
    ]
)
def test_cost_validity(gold: int, food: int, wood: int, stone: int, expected_return: bool):
    c = Cost(gold=gold, food=food, wood=wood, stone=stone)
    ret = c.is_valid()

    assert isinstance(ret, bool)
    assert ret == expected_return


@pytest.mark.parametrize(
    "first, second, expected_return",
    [
        # 1. Bad Cost
        (Cost("a", 0, 0, 0), Cost(1, 2, 3, 4), False),
        (Cost(0, [], 0, 0), Cost(1, 2, True, 4), False),
        (Cost(0, -1, 0, 0), Cost(1, 2, True, 4), False),
        (Cost(0, MAX_VALUE_LIMIT, 0, 0), Cost(1, 2, True, 4), False),

        # 2. Good Cost, True
        (Cost(0, 0, 0, 0), Cost(1, 2, 3, 4), True),
        (Cost(10, 20, 30), Cost(100, 22, 30, 40), True),
        (Cost(), Cost(), True),
        (Cost(1, 2, 3, 4), Cost(1, 2, 3, 4), True),

        # 3. Good Cost, False
        (Cost(10, 20, 30), Cost(), False),
        (Cost(1), Cost(0), False),
        (Cost(1), Cost(0, 1), False),
        (Cost(10), Cost(0, 10, 10, 10), False),
        (Cost(-1, 0, 0, 100), Cost(0, 10, 10, 1000), False),
    ]
)
def test_cost_can_create(first: Cost, second: Cost, expected_return: bool):
    assert isinstance(first, Cost)
    assert isinstance(second, Cost)
    assert (first < second) == expected_return


@pytest.mark.parametrize(
    "value, expected_output",
    [
        # 1. Invalid types
        (1, None),
        (None, None),
        ([], None),
        ({"a": 1, "b": "b"}, None),
        (Cost(), None),

        # 2. Valid types, bad formatting
        ("", None),
        ("0", None),
        ("1,2,3,4", None),
        ("[], {}, None, 'abcd'", None),
        ('{}', None),
        ("{'Gold': 100}", None),            # Bad quotes, attribute should be in single quote
        ('{"Gol": 299}', None),             # No attributes found
        ('{"Gold": 0}', None),              # No attributes > 0

        # 3. Valid parses
        ('{"Gold": 1}', Cost(gold=1)),
        ('{"Gold": 9, "Stone": 10}', Cost(gold=9, stone=10)),
        ('{"Gold": -1, "Stone": 10}', None),
        ('{"Gold": None, "Stone": 10}', None),
        ('{"Gold": [], "Stone": 10}', None),
        ('{"Gold": True, "Stone": 10}', None),
        ('{"Gold": aaa, "Stone": 10}', None),
        ('{"Gold": {}, "Stone": 10}', None),
        ('{"Gold": 9, "Stone": 10, "xyz": -1}', Cost(gold=9, stone=10)),
        ('{"Gold": 9, "Stone": 10, "xyz": 10}', Cost(gold=9, stone=10)),
        ('{"Gold": 9, "Stone": 10, "Wood": 0, "Food": 0}', Cost(gold=9, stone=10)),
        ('{"Gold": 9, "Stone": 10, "Wood": 4, "Food": 11}',
             Cost(gold=9, stone=10, wood=4, food=11)),
        ('{"Gold": 9, "Stone": 10, "Wood": 4, "Food": ' + str(MAX_VALUE_LIMIT) +'}',
             Cost(gold=9, stone=10, wood=4, food=MAX_VALUE_LIMIT)),
        ('{"Gold": 9, "Stone": 10, "Wood": 4, "Food": ' + str(MAX_VALUE_LIMIT + 1) + '}', None),
    ]
)
def test_cost_str_parser(value: str, expected_output: Cost):
    ret = Cost.from_str(value)
    assert isinstance(ret, Cost) or ret is None
    assert ret == expected_output
