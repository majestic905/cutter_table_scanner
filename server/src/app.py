import os
from flask import Flask


_root_path = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))
app = Flask(__name__, static_url_path='/', root_path=_root_path)
