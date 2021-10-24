from abc import ABC
from abc import abstractmethod


class Aoe2Parsable(ABC):

    """
    Abstract blueprint for an in-game parsable object,
    ex. Structure, Unit, Civilization etc
    """

    @staticmethod
    @abstractmethod
    def parse(self, *args):
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        pass

    @abstractmethod
    def can_create(self, cost) -> bool:
        pass
