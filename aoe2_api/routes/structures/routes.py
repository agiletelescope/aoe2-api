from flask import request
from flask import abort
from flask import jsonify
from flask import Blueprint

from aoe2_api.shared.statuscodes import *
from aoe2_api.models.cost import Cost
from aoe2_api.services.datastore import datastore

bp_structures = Blueprint('structures', __name__)


"""
Structures Routes
"""


@bp_structures.route('/')
def get_structures():
    """
    Retrieve a list of structures filtered by available cost, if any
    Request type: GET, body optional

    Body (optional),
    - gold: Int, amount of available Gold
    - food: Int, amount of available Food
    - wood: Int, amount of available Wood
    - stone: Int, amount of available Stone
    """

    # Process query filters, default to 0
    body = request.get_json() or {}
    available_cost = Cost.from_dict(body)

    if available_cost is None:
        abort(400, INVALID_DATA_FORMAT)
    if datastore is None:
        abort(400, DATA_STORE_BAD)

    data = datastore.filter_structures(cost=available_cost)
    return jsonify({"data": [s.to_json() for s in data]}), 201
