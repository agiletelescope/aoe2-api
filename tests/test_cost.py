import pytest

from aoe2_api.shared.config import *
from aoe2_api.models.cost import Cost


@pytest.mark.parametrize(
    "gold, food, wood, stone, expected_return",
    [
        # Gold
        (None, 1, 1, 1, True),
        ([], 1, 1, 1, False),
        ({}, 1, 1, 1, False),
        (True, 1, 1, 1, False),
        (Cost(), 1, 1, 1, False),
        ("a", 1, 1, 1, False),
        (MAX_VALUE_LIMIT + 1, 1, 1, 1, False),
        (MAX_VALUE_LIMIT, 1, 1, 1, True),

        # Food
        (1, None, 1, 1, True),
        (1, [], 1, 1, False),
        (1, {}, 1, 1, False),
        (1, True, 1, 1, False),
        (1, Cost(), 1, 1, False),
        (1, "a", 1, 1, False),
        (1, MAX_VALUE_LIMIT + 1, 1, 1, False),
        (1, MAX_VALUE_LIMIT, 1, 1, True),

        # Wood
        (1, 1, None, 1, True),
        (1, 1, [], 1, False),
        (1, 1, {}, 1, False),
        (1, 1, True, 1, False),
        (1, 1, Cost(), 1, False),
        (1, 1, "s", 1, False),
        (1, 1, MAX_VALUE_LIMIT + 1, 1, False),
        (1, 1, MAX_VALUE_LIMIT, 1, True),

        # Stone
        (1, 1, 1, None, True),
        (1, 1, 1, [], False),
        (1, 1, 1, {}, False),
        (1, 1, 1, True, False),
        (1, 1, 1, Cost(), False),
        (1, 1, 1, "s", False),
        (1, 1, 1, MAX_VALUE_LIMIT + 1, False),
        (1, 1, 1, MAX_VALUE_LIMIT, True),

        # Random
        (1, 0, 0, 0, True),
        (1, 1, 1, 1, True),
        ("a", 0, 0, 0, False),
        (0, [], 0, 0, False),
        (0, 0, {}, 0, False),
        (0, 0, 0, Cost(), False),
        (0, 0, True, 0, False),
        ("a", [], True, Cost(), False),
        (0, None, None, None, False),
        (None, None, None, None, False),
        (0, 0, 0, 0, False),                        # Empty cost
        (-1, -1929, 0, 0, False),                   # Gold value < 0
        (0, MAX_VALUE_LIMIT + 1, 0, 0, False),      # Food value > limit
        (0.21, 9.32, 88, 91, False),                # Decimal values
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
    "reqd, available, expected_return",
    [
        # Bad Cost
        (Cost("a", 0, 0, 0), Cost(1, 2, 3, 4), False),
        (Cost(0, [], 0, 0), Cost(1, 2, True, 4), False),
        (Cost(0, -1, 0, 0), Cost(1, 2, True, 4), False),
        (Cost(0, MAX_VALUE_LIMIT, 0, 0), Cost(1, 2, True, 4), False),
        (Cost(0, 0, 0, 0), Cost(1, 2, 3, 4), False),
        (Cost(), Cost(), False),
        (Cost(10, 20, 30), Cost(), False),

        # Good Cost, True
        (Cost(10, 20, 30), Cost(100, 22, 30, 40), True),
        (Cost(1, 2, 3, 4), Cost(1, 2, 3, 4), True),

        # Good Cost, False
        (Cost(1), Cost(0), False),
        (Cost(1), Cost(0, 1), False),
        (Cost(10), Cost(0, 10, 10, 10), False),
        (Cost(-1, 0, 0, 100), Cost(0, 10, 10, 1000), False),
    ]
)
def test_cost_can_create(reqd: Cost, available: Cost, expected_return: bool):
    assert isinstance(reqd, Cost)
    assert isinstance(available, Cost)
    assert (reqd.lte(available)) == expected_return


@pytest.mark.parametrize(
    "value, expected_output",
    [
        # Invalid types
        (1, None),
        (None, None),
        ([], None),
        ({"a": 1, "b": "b"}, None),
        (Cost(), None),

        # Valid types, bad formatting
        ("", None),
        ("0", None),
        ("1,2,3,4", None),
        ("[], {}, None, 'abcd'", None),
        ('{}', None),
        ("{'Gold': 100}", None),                    # Bad quotes, attribute should be in single quote
        ('{"Gol": 299}', None),                     # No attributes found
        ('{"Gold": 0}', None),                      # No attributes > 0

        # Valid parses
        ('{"Gold": 1}', Cost(gold=1)),
        ('{"Gold": 9, "Stone": 10}', Cost(gold=9, stone=10)),
        ('{"Gold": -1, "Stone": 10}', None),
        ('{"Gold": None, "Stone": 10}', None),
        ('{"Gold": [], "Stone": 10}', None),
        ('{"Gold": True, "Stone": 10}', None),
        ('{"Gold": aaa, "Stone": 10}', None),
        ('{"Gold": {}, "Stone": 10}', None),
        # Invalid json parse, extra ','
        ('{"Gold": 900,}', None),
        ('{"Gold": 9, "Stone": 10, "xyz": -1}', Cost(gold=9, stone=10)),
        ('{"Gold": 9, "Stone": 10, "Food": -1}', None),
        ('{"Gold": 9, "Stone": 10, "xyz": 10}', Cost(gold=9, stone=10)),
        ('{"Gold": 9, "Stone": 10, "Wood": 0, "Food": 0}', Cost(gold=9, stone=10)),
        # Repeating params => Last one is considered
        ('{"Gold": 9, "Stone": 10, "Wood": 4, "Food": 11, "Food": 110}',
         Cost(gold=9, stone=10, wood=4, food=110)),
        ('{"Gold": 9, "Stone": 10, "Wood": 4, "Food": ' + str(MAX_VALUE_LIMIT) + '}',
         Cost(gold=9, stone=10, wood=4, food=MAX_VALUE_LIMIT)),
        ('{"Gold": 9, "Stone": 10, "stone": 100}', Cost(gold=9, stone=10)),
        ('{"Gold": 9, "Stone": 10, "Wood": 4, "Food": ' + str(MAX_VALUE_LIMIT + 1) + '}', None),

        # Valid parses, with ; as the separator
        ('{"Gold": 9; "Stone": 10; "xyz": 10}', Cost(gold=9, stone=10)),
        ('{"Gold": 900;}', None),
        ('{"Gold": 9; "Stone": 10; "Stone": 100}', Cost(gold=9, stone=100)),
        ('{"Gold": 9; "Food": 10; "Stone": 100; "Wood": 1}', Cost(gold=9, stone=100, wood=1, food=10)),
    ]
)
def test_cost_str_parser(value: str, expected_output: Cost):
    ret = Cost.from_str(value)
    assert isinstance(ret, Cost) or ret is None
    assert ret == expected_output


@pytest.mark.parametrize(
    "value, expected_return",
    [
        # Invalid types
        (None, None),
        ([], None),
        (11, None),
        ("invalid", None),
        (True, None),

        # Types good
        ({}, None),
        ({"gold": 10, "random": 10}, Cost(gold=10)),
        ({"gold": 87, "wood": 92}, Cost(gold=87, wood=92)),
        ({"invalid1": 13, "invalid2": 83}, None),
        ({"gold": 13, "food": 83, "wood": 5, "stone": 88},
         Cost(gold=13, food=83, wood=5, stone=88)),
        ({"gold": 0, "food": 83, "wood": 5, "stone": 88},
         Cost(food=83, wood=5, stone=88)),
        ({"gold": -1, "food": 83, "wood": 5, "stone": 88}, None),
        ({"gold": 38, "food": [], "wood": 5, "stone": 88}, None),
        ({"gold": 38, "food": 199, "wood": True, "stone": 88}, None),
    ]
)
def test_cost_from_dict(value: dict, expected_return):
    c = Cost.from_dict(value)
    assert type(c) == Cost or c is None
    assert c == expected_return


@pytest.mark.parametrize(
    "cost1, cost2, expected_return",
    [
        # Bad cost
        (Cost(gold=[]), Cost(wood=1), False),
        (Cost(gold=1), Cost(wood="abcd"), False),
        (Cost(), Cost(food=100), False),
        (Cost(-1, 1, 1), Cost(-1, 1, 1), False),
        (Cost(1, MAX_VALUE_LIMIT + 1, 1), Cost(1, MAX_VALUE_LIMIT + 1, 1), False),
        (Cost(), Cost(), False),

        # Valid cost, bad comparison
        (Cost(gold=1), Cost(wood=1), False),
        (Cost(gold=1, wood=1), Cost(wood=1), False),
        (Cost(gold=1, wood=1), Cost(wood=1, stone=1), False),
        (Cost(1, 1, 1), Cost(wood=1, stone=1, food=1), False),

        # Good Comparison
        (Cost(1), Cost(1), True),
        (Cost(1, 1), Cost(1, 1), True),
        (Cost(1, 5), Cost(2, 10), True),
        (Cost(2, 5, 100), Cost(2, 5, 101), True),
        (Cost(1, 1, 1, 1), Cost(1, 1, 1, 1), True),
        (Cost(MAX_VALUE_LIMIT), Cost(MAX_VALUE_LIMIT), True),
    ]
)
def test_cost_comparison(cost1: Cost, cost2: Cost, expected_return: bool):
    assert isinstance(cost1, Cost) and isinstance(cost2, Cost)
    assert (cost1.lte(cost2)) == expected_return
