import os

"""
App Configurations
"""

# Build independent configs
DATA_DELIMITER = ","
DATA_COST_DELIMITER = ";"
MAX_VALUE_LIMIT = 5000


class DefaultConfig:

    # Flask App Configs
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.urandom(24)

    # Data Configs
    DATA_DIRECTORY = "data"
    STRUCTURES_DATA_FILE_PATH = DATA_DIRECTORY + "/structures.csv"
    UNITS_DATA_FILE_PATH = DATA_DIRECTORY + "/units.csv"


class DevConfig(DefaultConfig):
    DEBUG = True


class TestConfig(DefaultConfig):
    DEBUG = True
    TESTING = True

    # Test Data Configs
    DATA_DIRECTORY = "tests/data"
    STRUCTURES_DATA_FILE_PATH = DATA_DIRECTORY + "/mock_structures.csv"
    UNITS_DATA_FILE_PATH = DATA_DIRECTORY + "/mock_units.csv"
