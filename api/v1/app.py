#!/usr/bin/python3

from models import storage
from flask import Flask
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

@app.teardown_appcontext
def close_session(exception):
    """closes a session"""
    storage.colse()

if __name__ == "__main__":

    HOST = getenv('HBNB_API_HOST')
    PORT = getenv('HBNB_API_PORT')

    if not HOST: HOST = '0.0.0.0'
    if not PORT: PORT = 5000

    app.run(host=HOST, port=PORT, threaded=True)
