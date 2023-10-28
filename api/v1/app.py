#!/usr/bin/python3

from models import storage
from flask import Flask
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def close_session(exception):
    """closes a session"""
    storage.close()



@app.errorhandler(404)
def not_found(error):
    """
    handler for 404 errors that returns a JSON-formatted
    404 status code response
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":

    HOST = getenv('HBNB_API_HOST')
    PORT = getenv('HBNB_API_PORT')

    if not HOST: HOST = '0.0.0.0'
    if not PORT: PORT = 5000

    app.run(host=HOST, port=PORT, threaded=True)
