from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass

from aoe2_api.models.age import Age
from aoe2_api.models.cost import Cost
from aoe2_api.shared.config import *


@dataclass
class Aoe2Parsable(ABC):
    """
    Abstract blueprint for an in-game parsable object,
    ex. Structure, Unit, Civilization etc
    """

    name: str
    age: Age
    cost: Cost

    @staticmethod
    @abstractmethod
    def from_str(data):
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        are_types_valid = all([
            type(self.name) is str,
            isinstance(self.age, Age),
            isinstance(self.cost, Cost),
        ])
        if not are_types_valid:
            return False

        are_values_valid = all([
            self.name is not None,
            0 < len(self.name) <= MAX_VALUE_LIMIT,
            self.age is not None,
            self.cost.is_valid()
        ])
        return are_values_valid

    def to_json(self):
        """
        Generate a map of all keys to their values
        """

        return {k: self._get_val_repr(v)
                for k, v in vars(self).items()}

    def can_create(self, cost: Cost) -> bool:
        """
        Non abstract method, checks if this unit can be created
        """

        return self.cost.lte(cost)

    @staticmethod
    def _get_val_repr(value):
        """
        Return the representation of a given value in its json form
        """

        if type(value) is Cost:
            return value.to_json()
        if type(value) is Age:
            return str(value)

        return value
