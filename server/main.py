import time
import os
from flask import Flask, jsonify
from scans import get_scans_directory_tree

app = Flask(__name__, static_folder='../client/build', static_url_path='/')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/files')
def get_files():
    return jsonify(get_scans_directory_tree())