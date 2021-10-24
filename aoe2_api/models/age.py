from enum import Enum


class Age(Enum):

    """
    Age represents a period in civilization advancement,

    In aoe2 a civilization starts from Dark age, then progresses through Feudal,
    Castle and finally Imperial age.
    Age advancement provides the civilization with new units and technologies
    """

    DARK = 0
    FEUDAL = 1
    CASTLE = 2
    IMPERIAL = 3

    def is_dark(self):
        return self == self.DARK

    def is_feudal(self):
        return self == self.FEUDAL

    def is_castle(self):
        return self == self.CASTLE

    def is_imperial(self):
        return self == self.IMPERIAL
