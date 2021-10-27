from flask import Blueprint

bp_units = Blueprint('units', __name__)


@bp_units.route('/')
def get_units():
    return "units home"
