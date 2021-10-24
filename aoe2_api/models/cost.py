from dataclasses import dataclass


@dataclass
class Cost:

    """
    Resources required to build/produce a unit,
    Available resources include Gold, Stone, Wood and Food
    """

    gold: int = 0
    stone: int = 0
    wood: int = 0
    food: int = 0

    @staticmethod
    def parse(self, value: str):
        pass
