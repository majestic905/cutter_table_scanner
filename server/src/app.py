import os
from flask import Flask


_root_path = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))
app = Flask(__name__, root_path=_root_path)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-store, max-age=0"
    return response
