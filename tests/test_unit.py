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
        ("", Age.DARK, Cost(food=1), "d", "c", False),          # Empty name
        ("name", Age.DARK, Cost(food=1), "", "c", False),       # Empty description
        ("name", Age.DARK, Cost(food=1), "d", "", False),       # Empty created_in
        ("name", Age.CASTLE, Cost(), "d", "c", False),
        ("name", Age.CASTLE, Cost(gold=1), "d" * (MAX_VALUE_LIMIT + 1), "c", False),

        # 3. Valid cases
        ("name", Age.CASTLE, Cost(gold=1), "d" * MAX_VALUE_LIMIT, "c", True),
    ]
)
def test_unit_validity(name: str, age: Age, cost: Cost,
                       description: str, created_in: str, expected_return: bool):
    s = Unit(name, age, cost, description, created_in)
    ret = s.is_valid()

    assert isinstance(ret, bool)
    assert ret == expected_return
