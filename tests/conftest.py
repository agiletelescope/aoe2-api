import os
import sys

# Make server accessible for tests
api_dir = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.insert(0, api_dir)

from aoe2_api.models.age import Age
from aoe2_api.models.cost import Cost
from aoe2_api.models.unit import Unit
from aoe2_api.models.structure import Structure


# Mock Data
mock_structures = [
    Structure("a", Age.DARK, Cost(wood=175), 50, 1200),
    Structure("b", Age.FEUDAL, Cost(stone=150), 35, 1800),
    Structure("c", Age.CASTLE, Cost(gold=60), 15, 480),
    Structure("d", Age.DARK, Cost(food=60), 5, 48),
    Structure("e", Age.IMPERIAL, Cost(food=60, wood=10, gold=1, stone=9), 50, 800),
]
mock_units = [
    Unit("a", Age.FEUDAL, Cost(wood=2), "desc1", "building1"),
    Unit("b", Age.IMPERIAL, Cost(wood=25, gold=45), "desc2", "building2"),
    Unit("c", Age.CASTLE, Cost(wood=25, gold=45, stone=10), "desc3", "building2"),
    Unit("d", Age.FEUDAL, Cost(wood=25, gold=45), "desc4", "building2"),
    Unit("e", Age.DARK, Cost(wood=25, gold=45), "desc5", "building1"),
]
