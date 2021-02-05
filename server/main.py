import os.path
import repository
import scanner

from http import HTTPStatus as status
from flask import Flask, send_from_directory, request

app = Flask(__name__, static_folder='../client/build', static_url_path='/')



@app.route('/api/scans', methods=['GET'])
def get_scans():
    return {'scans': repository.index()}


@app.route('/api/scans/<name>', methods=['GET'])
def get_scan(name):
    file_path = repository.get(name)

    directory = os.path.dirname(file_path)
    kwargs = {
        'filename': os.path.basename(file_path),
        'as_attachment': bool(request.args.get('as_attachment')),
        'attachment_filename': f'{name}.jpg'
    }

    return send_from_directory(directory, **kwargs)


@app.route('/api/scans', methods=['POST'])
def post_scans():
    scanner.perform_scan()
    return '', status.OK


@app.route('/api/scans', methods=['DELETE'])
def delete_scans():
    repository.clear()
    return '', status.NO_CONTENT


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')
