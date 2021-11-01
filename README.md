
## aoe2-api
Simple aoe2 api written in python flask

#### Context
> Age of Empires II is a real-time strategy game that focuses on building towns, gathering resources, and creating armies to defeat opponents.  

In simple words, it's a game where in you gather resources (`gold, food, wood and stone`) distributed throughout the world, you can build a certain `structure` once you've gathered enough resources necessary to build it. Certain special structures (like Barracks) are capable of training/producing military `units` capable of attacking the enemy. More info about the game [here](https://en.wikipedia.org/wiki/Age_of_Empires_II).


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
│   ├── tests_cost.py              Tests for cost model
│   ├── tests_csvparser.py         Tests for csv parser
│   ├── tests_datastore.py         Tests for Datastore
│   ├── tests_structure.py         Tests for structure model
│   ├── tests_structures_api.py    Tests for structures routes, routes/structures/routes.py
│   ├── tests_unit.py              Tests for unit model
│   ├── tests_units_api.py         Tests for unit routes, routes/units/routes.py
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
    
#### Status Codes

```
SUCCESS = 0
```
```
# File Parser Errors
DATA_FILE_PATH_BAD = -1001
BLUEPRINT_BAD = -1002
```
```
# Request Errors
INVALID_DATA_FORMAT = -2001
```
```
# Internal Errors
DATA_STORE_BAD = -3001
```

## API

###### Body Params
Name | Type | Description
--- | --- | ---
`gold` | Integer | Available Gold, Optional
`food` | Integer | Available Food, Optional
`wood` | Integer | Available Wood, Optional
`stone` | Integer | Available Stone, Optional


###### Endpoints
Route | Request Type | Description
--- | --- | ---- 
`/structures` | `POST` | Retrieve all structures that match the body query
`/units`  | `POST` | Retrieve all units that match the body query

###### Success response format
```
{
  "data": [  ...  ]
}
```

###### Error response format
```
{
  "code": <Status Code of the error>,
  "message: <Description of the error>
}
```

### Examples
###### Success
Name | Value
--- | ---
Route | `/structures`
Request | `POST`
Body  | ``` { "gold": 10, "food": 20, "wood": 13, "stone": 5 } ```  

###### Response
```
{
    "data": [
        {
            "age": "feudal",
            "build_time_sec": 8,
            "cost": {
                "stone": 5
            },
            "hit_points": 1800,
            "name": "Stone Wall"
        },
        {
            "age": "castle",
            "build_time_sec": 8,
            "cost": {
                "stone": 5
            },
            "hit_points": 3000,
            "name": "Fortified Wall"
        }
    ]
}
```

###### Error
Name | Value
--- | ---
Route | `/structures`
Request | `POST`
Body  | ``` { "gold": -1 } ```  

###### Response
```
{
    "code": -2001,
    "message": "400 Bad Request: -2001"
}
```
