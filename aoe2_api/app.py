from flask import Flask
from flask import jsonify

from aoe2_api.shared.statuscodes import *
from aoe2_api.shared.config import DevConfig
from aoe2_api.shared.config import TestConfig
from aoe2_api.services.datastore import init_datastore


def create_app(is_testing=False):

    # Init Flask app
    flask_app = Flask(__name__)
    flask_app.config.from_object(
        TestConfig if is_testing else DevConfig)

    # Load data and init datastore
    ret = init_datastore(flask_app)
    if ret != SUCCESS:
        return None, ret

    # Post data load, init flask blueprints
    from aoe2_api.routes.structures.routes import bp_structures
    from aoe2_api.routes.units.routes import bp_units
    flask_app.register_blueprint(bp_structures, url_prefix="/structures")
    flask_app.register_blueprint(bp_units, url_prefix="/units")

    # Generic Error Handlers
    @flask_app.errorhandler(400)  # Bad request
    @flask_app.errorhandler(401)  # Un-authorized
    @flask_app.errorhandler(404)  # Not found
    @flask_app.errorhandler(405)  # method not allowed
    @flask_app.errorhandler(500)  # Internal server error
    def error_handler(e):
        return jsonify({'code': e.description, 'message': str(e)}), e.code

    return flask_app, SUCCESS
