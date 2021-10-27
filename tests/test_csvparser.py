import pytest

from aoe2_api.shared.config import *
from aoe2_api.shared.config import TestConfig
from aoe2_api.shared.statuscodes import *
from aoe2_api.models.cost import Cost
from aoe2_api.models.unit import Unit
from aoe2_api.models.structure import Structure
from aoe2_api.services.csvparser import CsvParser

from tests.conftest import mock_structures
from tests.conftest import mock_units

# Helper constants
_valid_blueprint = Structure
_valid_filename = TestConfig.STRUCTURES_DATA_FILE_PATH
_ret_filename_bad = (None, DATA_FILE_PATH_BAD)
_ret_blueprint_bad = (None, BLUEPRINT_BAD)


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

        # All Valid
        (_valid_filename, _valid_blueprint, (mock_structures, SUCCESS)),
        (_valid_filename, Structure, (mock_structures, SUCCESS)),
        (TestConfig.UNITS_DATA_FILE_PATH, Unit, (mock_units, SUCCESS)),
    ]
)
def test_csv_parser(filename: str, blueprint, expected_output):
    c = CsvParser(filename, blueprint)
    assert isinstance(c, CsvParser)

    ret = c.parse_file()
    assert ret == expected_output
