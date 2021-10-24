import json
from dataclasses import dataclass
from json.decoder import JSONDecodeError

from aoe2_api.shared.config import *


@dataclass
class Cost:
    """
    Resources required to build/produce a unit,
    Resource type include Gold, Food, Wood and Stone
    """

    gold: int = None
    food: int = None
    wood: int = None
    stone: int = None

    def __post_init__(self) -> None:
        self.gold = 0 if self.gold is None else self.gold
        self.food = 0 if self.food is None else self.food
        self.wood = 0 if self.wood is None else self.wood
        self.stone = 0 if self.stone is None else self.stone

    def __lt__(self, other) -> bool:
        """
        Check if the provided resources are enough to produce a unit/structure

        :param other: Cost, cost available
        :return: Boolean, True if unit can be produced, False otherwise
        """

        if not other.is_valid() or \
                not self.is_valid():
            return False

        return other.gold >= self.gold and \
               other.stone >= self.stone and \
               other.wood >= self.wood and \
               other.stone >= self.stone

    def is_valid(self) -> bool:
        """
        datatype and limit validation

        :return: Boolean, True if resources values are valid,
                 False otherwise
        """
        are_types_valid = all([
            type(self.gold) is int,
            type(self.food) is int,
            type(self.wood) is int,
            type(self.stone) is int,
            ])
        if not are_types_valid:
            return False

        are_values_valid = all([
            0 <= self.gold <= MAX_VALUE_LIMIT,
            0 <= self.food <= MAX_VALUE_LIMIT,
            0 <= self.wood <= MAX_VALUE_LIMIT,
            0 <= self.stone <= MAX_VALUE_LIMIT
        ])
        return are_values_valid

    @staticmethod
    def from_str(value: str):
        """
        Parse the string to obtain the cost values.
        From data this is of the format {resource1: value1; resource2: value2}
        where delimiter is ";"

        :param value: the string that needs to be parsed
        :return: Cost object if parse successful, None otherwise
        """

        if not isinstance(value, str):
            return

        try:
            value = json.loads(
                value.replace(DATA_COST_DELIMITER, DATA_DELIMITER))
            cost = Cost(
                int(value.get("Gold", 0)),
                int(value.get("Food", 0)),
                int(value.get("Wood", 0)),
                int(value.get("Stone", 0))
            )

            # cost != Cost() ensures that not all parsed attributes were wrong or 0
            if cost.is_valid() and cost != Cost():
                return cost
        except (TypeError, ValueError, JSONDecodeError, AttributeError):
            # ValueError, dict values aren't int
            # JSONDecodeError, Json parse error
            # AttributeError, attempt to call .get() on a non-dict obj
            return
