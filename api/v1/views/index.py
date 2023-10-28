#!/usr/bin/python3
"""
This module displays the status
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    """ returns Json status OK """
    return jsonify({"status": "OK"})
