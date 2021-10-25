from dataclasses import dataclass

from aoe2_api.shared.config import *
from aoe2_api.models.age import Age
from aoe2_api.models.cost import Cost
from aoe2_api.models.aoe2parsable import Aoe2Parsable


@dataclass
class Structure(Aoe2Parsable):

    """
    Refers to a constructable building in aoe2
    """

    build_time_sec: int
    hit_points: int

    def is_valid(self) -> bool:
        if not super().is_valid():
            return False

        are_types_valid = all([
            type(self.build_time_sec) is int,
            type(self.hit_points) is int,
        ])
        if not are_types_valid:
            return False

        # Build time could be 0
        # Hit points has to be greater than 0 for the unit to exist
        are_values_valid = all([
            0 <= self.build_time_sec <= MAX_VALUE_LIMIT,
            0 < self.hit_points <= MAX_VALUE_LIMIT
        ])
        return are_values_valid

    @staticmethod
    def from_str(data):

        if not isinstance(data, str):
            return

        try:
            name, age, cost, build_time_sec, hit_points = \
                data.split(DATA_DELIMITER)
            age = Age.from_str(age.strip())
            cost = Cost.from_str(cost.strip())
            build_time_sec = int(build_time_sec.strip())
            hit_points = int(hit_points.strip())

            parsed = Structure(name, age, cost, build_time_sec, hit_points)

            return parsed \
                if parsed.is_valid() else None
        except (TypeError, ValueError):
            return
