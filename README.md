
## aoe2-api
Simple aoe2 api written in python flask

#### Project Structure
```
.
├── aoe2_api                       The aoe2-api application
│   ├── shared                     Modules shared throughout the application
│   │   ├── config.py              Application configuraitons
│   │   ├── utils.py               Utility functions & decorators
│   │   └── statuscodes.py         Status/Error codes returned by application
│   ├── models                     Object models
│   │   ├── age.py                 Civilization Age model
│   │   ├── aoe2parsable.py        Aoe2 parsable object blueprint
│   │   ├── cost.py                Resources Cost model
│   │   ├── structure.py           Aoe2 structure/building model
│   │   └── unit.py                Aoe2 unit model
│   ├── routes                     Flask Blueprints
│   │   ├── structures             Blueprints for structures api
│   │   └── unit                   Blueprints for units api
│   ├── services                   Functional application components
│   │   ├── csvparser.py           Csv file parser
│   │   └── datastore.py           Datastore, handles data loading and filtering
│   ├── data                       Api data container
│   │   ├── structures.csv         Structures csv data file
│   │   └── units.csv              Units csv data file
│   └── app.py                     Flask app creation & initialization
├── tests                          Pytest Container
│   ├── data                       Predefined data files, used for tests
│   ├── tests_cost.py              pytest songs service
│   ├── tests_csvparser.py         pytest users service
│   ├── tests_datastore.py         pytest songs service
│   ├── tests_structure.py         pytest songs service
│   ├── tests_structures_api.py    pytest songs service
│   ├── tests_unit.py              pytest songs service
│   ├── tests_units_api.py         pytest songs service
│   └── conftest.py                pytest init and fixtures definition
└── run.py                         Callable entry point to run the server
```

#### Usage
- Clone project
    ```
    git clone https://github.com/agiletelescope/aoe2-api
    cd aoe2-api
    ```
- Create a virtual env
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```
- Install requirements
    ```
    pip3 install -r requirements.txt
    ```
- Run server
    ```
    python3 run.py
    ```
- To run tests
    ```
    pytest -vvs
    ```
- Edit application configs
    ```
    vim ./aoe2_api/shared/config.py
    ```
