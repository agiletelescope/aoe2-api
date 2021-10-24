from dataclasses import dataclass

from aoe2_api.shared.config import *


@dataclass
class Cost:
    """
    Resources required to build/produce a unit,
    Available resources include Gold, Food, Wood and Stone
    """

    gold: int = None
    food: int = None
    wood: int = None
    stone: int = None

    def __post_init__(self):
        self.gold = 0 if self.gold is None else self.gold
        self.food = 0 if self.food is None else self.food
        self.wood = 0 if self.wood is None else self.wood
        self.stone = 0 if self.stone is None else self.stone

    @staticmethod
    def parse(self, value: str):
        pass

    def is_valid(self):
        """
        datatype and limit validation

        :return: Boolean, True if resources values are valid,
                 False otherwise
        """
        is_types_valid = all([
            type(self.gold) is int,
            type(self.food) is int,
            type(self.wood) is int,
            type(self.stone) is int,
        ])
        if not is_types_valid:
            return False

        is_value_valid = all([
            0 <= self.gold <= MAX_RESOURCE_LIMIT,
            0 <= self.food <= MAX_RESOURCE_LIMIT,
            0 <= self.wood <= MAX_RESOURCE_LIMIT,
            0 <= self.stone <= MAX_RESOURCE_LIMIT
        ])
        return is_value_valid

    def can_create(self, available) -> bool:
        """
        Check if the provided resources are enough to produce a unit/structure

        :param available: Cost, cost available
        :return: Boolean, True if unit can be produced, False otherwise
        """

        if not available.is_valid() or \
                not self.is_valid():
            return False

        return available.gold >= self.gold and \
               available.stone >= self.stone and \
               available.wood >= self.wood and \
               available.stone >= self.stone

    @staticmethod
    def copy_with(second):
        if second is None:
            return
        if not isinstance(second, Cost):
            return

        return Cost(
            second.gold, second.food,
            second.wood, second.stone
        )
