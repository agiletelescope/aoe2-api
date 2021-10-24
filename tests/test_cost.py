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
        (0, MAX_RESOURCE_LIMIT + 1, 0, 0, False),      # Food value > limit
        (0.21, 9.32, 88, 91, False),                   # Decimal values

        # 4. Valid cases
        (0, 0, 0, 0, True),
        (10, 20, 88, 91, True),
        (1000, 0, MAX_RESOURCE_LIMIT - 1, 0, True),
        (10, 20, MAX_RESOURCE_LIMIT, 91, True),
    ]
)
def test_cost_validity(gold: int, food: int, wood: int, stone: int, expected_return: bool):
    c = Cost(gold=gold, food=food, wood=wood, stone=stone)
    assert c.is_valid() == expected_return


@pytest.mark.parametrize(
    "first, second, expected_return",
    [
        # 1. Bad Cost
        (Cost("a", 0, 0, 0), Cost(1, 2, 3, 4), False),
        (Cost(0, [], 0, 0), Cost(1, 2, True, 4), False),
        (Cost(0, -1, 0, 0), Cost(1, 2, True, 4), False),
        (Cost(0, MAX_RESOURCE_LIMIT, 0, 0), Cost(1, 2, True, 4), False),

        # 2. Good Cost, True
        (Cost(0, 0, 0, 0), Cost(1, 2, 3, 4), True),
        (Cost(10, 20, 30), Cost(100, 22, 30, 40), True),
        (Cost(), Cost(), True),

        # 3. Good Cost, False
        (Cost(10, 20, 30), Cost(), False),
        (Cost(1), Cost(0), False),
        (Cost(1), Cost(0, 1), False),
        (Cost(10), Cost(0, 10, 10, 10), False),
        (Cost(-1, 0, 0, 100), Cost(0, 10, 10, 1000), False),
    ]
)
def test_cost_can_create(first: Cost, second: Cost, expected_return: bool):
    assert first.can_create(second) == expected_return
