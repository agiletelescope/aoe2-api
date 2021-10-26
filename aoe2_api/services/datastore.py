from aoe2_api.shared.config import *
from aoe2_api.shared.statuscodes import *
from aoe2_api.models.structure import Structure
from aoe2_api.models.unit import Unit
from aoe2_api.models.cost import Cost
from aoe2_api.services.csvparser import CsvParser


class DataStore:

    """
    Emulates the Database,
    Responsible for parsing the csv data files and storing the data
    """

    def __init__(self):
        self.structure_parser = CsvParser(STRUCTURES_DATA_FILE_PATH, Structure)
        self.unit_parser = CsvParser(UNITS_DATA_FILE_PATH, Unit)

        self.structures = []
        self.units = []

    def load_data(self) -> None:
        """
        Parse data from csv files and store them.
        :return: StatusCode, 0 if successful else error code
        """

        ret, structures = self.structure_parser.parse_file()
        if ret != SUCCESS:
            return ret

        ret, units = self.unit_parser.parse_file()
        if ret != SUCCESS:
            return ret

        self.structures = structures
        self.units = units
        return SUCCESS

    def filter_structures(self, cost: Cost) -> list:
        """
        Get a list of all structures that can be built with
            "cost" amount of resources

        :param cost: Cost, available resources
        :return: List of structures
        """

        return [s.cost.lte(cost) for s in self.structures]

    def filter_units(self, cost: Cost) -> list:
        """
        Get a list of all unit that can be created with
            "cost" amount of resources

        :param cost: Cost, available resources
        :return: List of units
        """

        return [u.cost.lte(cost) for u in self.units]
