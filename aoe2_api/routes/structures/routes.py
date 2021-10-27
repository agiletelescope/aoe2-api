from flask import request
from flask import abort
from flask import jsonify
from flask import Blueprint

from aoe2_api.shared.statuscodes import *
from aoe2_api.models.cost import Cost
from aoe2_api.services.datastore import s_datastore

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
    gold = body.get('gold') or 0
    food = body.get('food') or 0
    wood = body.get('wood') or 0
    stone = body.get('stone') or 0

    available_cost = Cost(
        gold=gold, food=food, wood=wood, stone=stone)
    if not available_cost.is_valid():
        abort(400, INVALID_DATA_FORMAT)
    if s_datastore is None:
        abort(400, DATA_STORE_BAD)

    return jsonify({"data": "data"}), 201
