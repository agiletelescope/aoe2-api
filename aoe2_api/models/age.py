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

    mapping = {
        DARK: "Dark",
        FEUDAL: "Feudal",
        CASTLE: "Castle",
        IMPERIAL: "Imperial"
    }

    def get_str_repr(self) -> list:
        """
        Return all possible string representation of the current age

        :return: List of all strings that are a valid
                 representation of the current age
        """

        mapping = {
            self.DARK: "dark",
            self.FEUDAL: "feudal",
            self.CASTLE: "castle",
            self.IMPERIAL: "imperial"
        }
        value = mapping[self] if self in mapping else ""

        # Example, when dark age, return ["dark", "Dark", "DARK"]
        return [value, value.title(), value.upper()]

    def is_dark(self) -> bool:
        return self == self.DARK

    def is_feudal(self) -> bool:
        return self == self.FEUDAL

    def is_castle(self) -> bool:
        return self == self.CASTLE

    def is_imperial(self) -> bool:
        return self == self.IMPERIAL

    @staticmethod
    def from_str(value: str):
        """
        Parse string to Age value

        :param value: String, denoting the civilization age
        :return: Age if parse successful, None otherwise
        """
        if value in Age.DARK.get_str_repr():
            return Age.DARK
        elif value in Age.FEUDAL.get_str_repr():
            return Age.FEUDAL
        elif value in Age.CASTLE.get_str_repr():
            return Age.CASTLE
        elif value in Age.IMPERIAL.get_str_repr():
            return Age.IMPERIAL

        # No match found
        return
