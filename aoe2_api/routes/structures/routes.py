from flask import Blueprint

bp_structures = Blueprint('structures', __name__)


@bp_structures.route('/')
def get_structures():
    return "structures home"
