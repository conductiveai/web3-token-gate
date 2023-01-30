"""
    This file is meant to help with testing by emulating the way Google Cloud Functions work.
    It will dispatch incoming requests to entrypoint function in a similar manner to how
    GCF would do it.
"""

from flask import Flask, request

from main import entrypoint
from flask_cors import cross_origin

app = Flask(__name__)


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin(
        origins=["http://localhost:8080"],
        methods=['GET', 'POST', 'OPTIONS'],
        allow_headers=['authorization', 'Content-Type'],
        automatic_options=True
    )
def index(path):
    return entrypoint(request)


app.run(debug=True, port=8000, host='0.0.0.0')
