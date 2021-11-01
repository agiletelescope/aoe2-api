from dataclasses import dataclass

from aoe2_api.shared.config import *
from aoe2_api.models.age import Age
from aoe2_api.models.cost import Cost
from aoe2_api.models.aoe2parsable import Aoe2Parsable


@dataclass
class Unit(Aoe2Parsable):

    """
    Units are train-ables that can be created from specific buildings
    Ex, military buildings can create military troops
    """

    description: str
    created_in: str

    def is_valid(self) -> bool:
        """
        Check if the Unit object is valid

        :return: Boolean, True if valid, False otherwise
        """

        if not super().is_valid():
            return False

        are_types_valid = all([
            type(self.description) is str,
            type(self.created_in) is str,
            ])
        if not are_types_valid:
            return False

        are_values_valid = all([
            0 < len(self.description) <= MAX_VALUE_LIMIT,
            0 < len(self.created_in) <= MAX_VALUE_LIMIT
        ])
        return are_values_valid

    @staticmethod
    def from_str(data):
        """
        Parse a string to object a Structure
        """

        if not isinstance(data, str):
            return

        try:
            name, age, cost, description, created_in = \
                data.split(DATA_DELIMITER)
            age = Age.from_str(age.strip())
            cost = Cost.from_str(cost.strip())

            parsed = Unit(name, age, cost,
                          description.strip(), created_in.strip())

            return parsed \
                if parsed.is_valid() else None
        except (TypeError, ValueError):
            return
