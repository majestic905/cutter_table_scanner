import os
from flask import Flask


_root_path = os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir))
app = Flask(__name__, root_path=_root_path)
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
