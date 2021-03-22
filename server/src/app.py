import os
from flask import Flask

app = Flask(__name__, static_url_path='/', root_path=os.path.join(os.path.dirname(__file__), os.pardir))
