from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass

from aoe2_api.models.age import Age
from aoe2_api.models.cost import Cost


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
    def from_str(*args):
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
            len(self.name) > 0,
            self.age is not None,
            self.cost.is_valid()
        ])
        return are_values_valid

    def can_create(self, cost: Cost) -> bool:
        """
        Non abstract method, checks if this unit can be created
        """
        return self.cost < cost
