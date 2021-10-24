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

        # 2. Bad values
        (-1, -1929, 0, 0, False),                      # Gold value < 0
        (0, MAX_RESOURCE_LIMIT + 1, 0, 0, False),  # Food value > limit
        (0.21, 9.32, 88, 91, False),               # Decimal values

        # 3. Valid cases
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
        # Bad cost
        (Cost("a", 0, 0, 0), Cost(1, 2, 3, 4), False),
        (Cost(0, [], 0, 0), Cost(1, 2, True, 4), False)
    ]
)
def test_cost_can_create(first: Cost, second: Cost, expected_return: bool):
    assert first.can_create(second) == expected_return
