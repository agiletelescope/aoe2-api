from flask import Flask


def create_app():

    # Init Flask app
    flask_app = Flask(__name__)

    # Routes
    @flask_app.route("/")
    def homepage():
        return "home"

    return flask_app
