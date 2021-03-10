import json
from datetime import datetime
from http import HTTPStatus as status
from flask import request

from settings import get_settings, save_settings, validate_settings
from cameras import update_cameras
from scan import Scan, ScanType
from scanner import build_snapshot, build_calibration
from app import app


@app.errorhandler(404)
def resource_not_found(e):
    return {"message": str(e)}, 404


@app.route('/api/scans', methods=['GET'])
def get_scans():
    scans = []

    for scan_id in Scan.ids():
        scan = Scan.find_by_id(scan_id, check_existence=False)
        scans.append({
            'scanId': scan.id,
            'scanType': scan.type.name,  # it's important to send .name, see Scan.find_by_id
            'createdAt': datetime.fromtimestamp(int(scan.timestamp)).strftime('%d %B %Y, %H:%M'),
            'images': scan.urls
        })

    return {'scans': list(reversed(scans))}


@app.route('/api/scans', methods=['POST'])
def post_scans():
    try:
        scan_type = request.args.get('type')
    except KeyError:
        return {'message': 'Wrong `type` value'}, status.BAD_REQUEST

    if scan_type == ScanType.SNAPSHOT:
        build_snapshot()
    elif scan_type == ScanType.CALIBRATION:
        build_calibration()

    return '', status.NO_CONTENT


@app.route('/api/scans', methods=['DELETE'])
def delete_scans():
    Scan.delete_all()
    return '', status.NO_CONTENT


############


@app.route('/api/settings', methods=['GET'])
def get_settings_handle():
    return get_settings()


@app.route('/api/settings', methods=['POST'])
def post_settings():
    error_msg = validate_settings(request.json)
    if error_msg is not None:
        return {'message': error_msg}, status.BAD_REQUEST

    save_settings(request.json)
    update_cameras()

    return '', status.NO_CONTENT


############


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('build/index.html')
