import os.path
import storage
import scanner
from scan import ScanFile

from http import HTTPStatus as status
from flask import Flask, send_from_directory, request

app = Flask(__name__, static_folder='../client/build', static_url_path='/')



@app.route('/api/scans', methods=['GET'])
def get_scans():
    return storage.scans_list()


@app.route('/api/scans/<scan_id>', methods=['GET'])
def get_scan(scan_id):
    file_path = storage.path_for_scan_file(scan_id, ScanFile.RESULT)

    directory = os.path.dirname(file_path)
    kwargs = {
        'filename': os.path.basename(file_path),
        'as_attachment': bool(request.args.get('as_attachment')),
        'attachment_filename': f'{scan_id}.jpg'
    }

    return send_from_directory(directory, **kwargs)


@app.route('/api/scans', methods=['POST'])
def post_scans():
    scanner.perform_scan()
    return '', status.OK


@app.route('/api/scans', methods=['DELETE'])
def delete_scans():
    storage.clear_scans_dir()
    return '', status.NO_CONTENT


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')
