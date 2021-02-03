import time
import os
from http import HTTPStatus as status
from flask import Flask
from scans import get_scans_directories_list, delete_scans_directories, create_example_scans

app = Flask(__name__, static_folder='../client/build', static_url_path='/')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/scans', methods=['GET'])
def get_scans():
    return {'scans': get_scans_directories_list()}


@app.route('/api/scans', methods=['DELETE'])
def delete_scans():
    delete_scans_directories()
    return '', status.NO_CONTENT


@app.route('/api/scans', methods=['POST'])
def create_scans():
    create_example_scans()
    return '', status.OK