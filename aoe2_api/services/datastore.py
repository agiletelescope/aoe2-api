from aoe2_api.shared.statuscodes import *
from aoe2_api.shared.config import DefaultConfig
from aoe2_api.models.structure import Structure
from aoe2_api.models.unit import Unit
from aoe2_api.models.cost import Cost
from aoe2_api.services.csvparser import CsvParser


class DataStore:

    """
    Emulates the Database,
    Responsible for parsing the csv data files and storing the data
    """

    def __init__(self, flask_app):

        # Load the file path configs
        s_file_path = DefaultConfig.STRUCTURES_DATA_FILE_PATH
        u_file_path = DefaultConfig.UNITS_DATA_FILE_PATH
        if flask_app is not None:
            s_file_path = flask_app.config["STRUCTURES_DATA_FILE_PATH"]
            u_file_path = flask_app.config["UNITS_DATA_FILE_PATH"]

        self.structure_parser = CsvParser(s_file_path, Structure)
        self.unit_parser = CsvParser(u_file_path, Unit)

        self.structures = []
        self.units = []

    def load_data(self) -> int:
        """
        Parse data from csv files and store them.
        :return: StatusCode, 0 if successful else error code
        """

        structures, ret = self.structure_parser.parse_file()
        if ret != SUCCESS:
            return ret

        units, ret = self.unit_parser.parse_file()
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

        if not isinstance(cost, Cost):
            return []
        if not cost.is_valid():
            return []

        return list(filter(lambda s: s.can_create(cost), self.structures))

    def filter_units(self, cost: Cost) -> list:
        """
        Get a list of all unit that can be created with
            "cost" amount of resources

        :param cost: Cost, available resources
        :return: List of units
        """

        if not isinstance(cost, Cost):
            return []
        if not cost.is_valid():
            return []

        return list(filter(lambda u: u.can_create(cost), self.units))


def init_datastore(flask_app) -> int:
    global datastore
    if datastore is not None:
        # Datastore already initialized
        return SUCCESS

    datastore = DataStore(flask_app)
    return datastore.load_data()


"""
Singleton DataStore Instance
"""
datastore = None
