from pathlib import Path
from flask import Flask


app = Flask(__name__, root_path=str(Path(__file__).parent.parent.parent), static_url_path='/')


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-store, max-age=0"
    return response
