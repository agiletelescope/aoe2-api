import os.path
import inspect

from aoe2_api.models.aoe2parsable import Aoe2Parsable
from aoe2_api.shared.statuscodes import *


class CsvParser:

    """
    Map a csv data file to a model
    """

    def __init__(self, filename, blueprint):
        self.filename = filename
        self.blueprint = blueprint

    def _validate_filename(self):
        if self.filename is None:
            return False
        if not type(self.filename) is str:
            return False
        if not os.path.isfile(self.filename):
            return False

        return True

    def _validate_blueprint(self):
        if self.blueprint is None:
            return False
        if not inspect.isclass(self.blueprint):
            return False

        # Blueprint has to be one of the parsable overrides
        if not issubclass(self.blueprint, Aoe2Parsable):
            return False

        return True

    def parse_file(self):
        if not self._validate_filename():
            return None, DATA_FILE_PATH_BAD
        if not self._validate_blueprint():
            return None, BLUEPRINT_BAD

        items = []
        with open(self.filename, "r") as f:
            lines = f.readlines()
            for line in lines:
                item = self.blueprint.from_str(line)

                if item is not None:
                    items.append(item)

        return items, SUCCESS
