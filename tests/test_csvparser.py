import pytest

from aoe2_api.shared.config import *
from aoe2_api.shared.statuscodes import *
from aoe2_api.models.age import Age
from aoe2_api.models.cost import Cost
from aoe2_api.models.unit import Unit
from aoe2_api.models.structure import Structure
from aoe2_api.services.csvparser import CsvParser

# Helper constants
_valid_blueprint = Structure
_valid_filename = MOCK_STRUCTURES_FILE_PATH
_ret_filename_bad = (None, DATA_FILE_PATH_BAD)
_ret_blueprint_bad = (None, BLUEPRINT_BAD)
_mock_structures = [
    Structure("a", Age.DARK, Cost(wood=175), 50, 1200),
    Structure("b", Age.FEUDAL, Cost(stone=150), 35, 1800),
    Structure("c", Age.CASTLE, Cost(gold=60), 15, 480),
    Structure("d", Age.DARK, Cost(food=60), 5, 48),
    Structure("e", Age.IMPERIAL, Cost(food=60, wood=10, gold=1, stone=9), 50, 800),
]
_mock_units = [
    Unit("a", Age.FEUDAL, Cost(wood=2), "building1", "desc1"),
    Unit("b", Age.IMPERIAL, Cost(wood=25, gold=45), "building2", "desc2"),
    Unit("c", Age.CASTLE, Cost(wood=25, gold=45, stone=10), "building2", "desc3"),
    Unit("d", Age.FEUDAL, Cost(wood=25, gold=45), "building2", "desc4"),
    Unit("e", Age.DARK, Cost(wood=25, gold=45), "building1", "desc5"),
]


@pytest.mark.parametrize(
    "filename, blueprint, expected_output",
    [
        # Filename
        (None, _valid_blueprint, _ret_filename_bad),
        (1, _valid_blueprint, _ret_filename_bad),
        (True, _valid_blueprint, _ret_filename_bad),
        ([], _valid_blueprint, _ret_filename_bad),
        ({}, _valid_blueprint, _ret_filename_bad),
        ("", _valid_blueprint, _ret_filename_bad),
        ("a"*MAX_VALUE_LIMIT, _valid_blueprint, _ret_filename_bad),

        # Blueprint
        (_valid_filename, None, _ret_blueprint_bad),
        (_valid_filename, 1, _ret_blueprint_bad),
        (_valid_filename, True, _ret_blueprint_bad),
        (_valid_filename, [], _ret_blueprint_bad),
        (_valid_filename, {}, _ret_blueprint_bad),
        (_valid_filename, "", _ret_blueprint_bad),
        (_valid_filename, Cost(), _ret_blueprint_bad),
        (_valid_filename, Cost, _ret_blueprint_bad),
        (_valid_filename, Structure, (_mock_structures, SUCCESS)),
        (MOCK_UNITS_DATA_FILE_PATH, Unit, (_mock_units, SUCCESS)),

        # All Valid
        (_valid_filename, _valid_blueprint, (_mock_structures, SUCCESS))
    ]
)
def test_csv_parser(filename: str, blueprint, expected_output):
    c = CsvParser(filename, blueprint)
    assert isinstance(c, CsvParser)

    ret = c.parse_file()
    assert ret == expected_output
