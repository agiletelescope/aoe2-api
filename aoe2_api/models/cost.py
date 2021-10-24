from dataclasses import dataclass

from aoe2_api.shared.config import *


@dataclass
class Cost:
    """
    Resources required to build/produce a unit,
    Available resources include Gold, Food, Wood and Stone
    """

    gold: int = 0
    food: int = 0
    wood: int = 0
    stone: int = 0

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
            isinstance(self.gold, int),
            isinstance(self.food, int),
            isinstance(self.wood, int),
            isinstance(self.stone, int),
        ])

        is_value_valid = all([
            0 <= self.gold <= MAX_RESOURCE_LIMIT,
            0 <= self.food <= MAX_RESOURCE_LIMIT,
            0 <= self.wood <= MAX_RESOURCE_LIMIT,
            0 <= self.stone <= MAX_RESOURCE_LIMIT
        ])

        return is_types_valid and is_value_valid

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
