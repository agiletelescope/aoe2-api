from aoe2_api.app import create_app


"""
Entry point, 
Runs the flask app
"""


if __name__ == "__main__":
    app, ret = create_app()
    if app is None:
        print("Error starting server, code: ", ret)
        exit(0)

    app.run()
