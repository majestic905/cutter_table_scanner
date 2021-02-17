import os.path
from scan import Scan
from scanner import Scanner
from enums import ScanFile, ScanType

from http import HTTPStatus as status
from flask import Flask, send_from_directory, request

app = Flask(__name__, static_folder='../client/build', static_url_path='/')


@app.route('/api/scans', methods=['GET'])
def get_scans():
    return {'scans': Scan.list_all()}


@app.route('/api/scans/<scan_id>', methods=['GET'])
def get_scan(scan_id):
    scan = Scan.find(scan_id)
    file_path = scan.path_for(ScanFile.RESULT)

    directory = os.path.dirname(file_path)
    kwargs = {
        'filename': os.path.basename(file_path),
        'as_attachment': bool(request.args.get('as_attachment')),
        'attachment_filename': f'{scan_id}.jpg'
    }

    return send_from_directory(directory, **kwargs)


@app.route('/api/scans', methods=['POST'])
def post_scans():
    scan = Scan.new(ScanType.SNAPSHOT)
    scanner = Scanner(scan)
    scanner.make_snapshot()
    return '', status.OK


@app.route('/api/scans', methods=['DELETE'])
def delete_scans():
    Scan.delete_all()
    return '', status.NO_CONTENT


@app.route('/api/cameras/projection_points/calibrate', methods=['POST'])
def camera_projection_points_calibrate():
    scan = Scan.new(ScanType.CALIBRATION)
    scanner = Scanner(scan)
    scanner.make_calibration_images()
    return '', status.OK


# @app.route('/api/cameras/projection_points', methods=['POST'])
# def camera_projection_points_set():
#     scanner = Scanner()
#     scanner.perform_calibration()
#     return '', status.OK


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')
