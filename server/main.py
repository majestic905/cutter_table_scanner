import json
from datetime import datetime
from http import HTTPStatus as status
from flask import request

from settings import get_settings, save_settings
from cameras import update_cameras
from scan import Scan
from scanner import Scanner
from server.constants.enums import ScanFile, ScanType, ImageLevel
from app import app




@app.route('/api/scans', methods=['GET'])
def get_scans():
    scans = []

    for scan_id in Scan.ids():
        scan = Scan.find_by_id(scan_id, check_existence=False)

        item = {
            'scanId': scan.id,
            'scanType': scan.type.name,  # it's important to send .name, see Scan.find_by_id
            'createdAt': datetime.fromtimestamp(int(scan.timestamp)).strftime('%d %B %Y, %H:%M'),
            'images': {}
        }

        image_levels = ImageLevel.__members__.values()
        if scan.type == ScanType.CALIBRATION:
            image_levels = [ImageLevel.ORIGINAL, ImageLevel.UNDISTORTED]

        images = {level: scan.urls_for_image_level(level) for level in image_levels}
        for image_level in images:
            item['images'][image_level.name] = {}
            for camera_position in images[image_level]:
                item['images'][image_level.name][camera_position.name] = images[image_level][camera_position]

        if scan.type == ScanType.SNAPSHOT:
            item['images'][ScanFile.RESULT.name] = scan.url_for(ScanFile.RESULT)

        scans.append(item)

    return {'scans': list(reversed(scans))}


@app.route('/api/scans', methods=['POST'])
def post_scans():
    try:
        scan_type = ScanType[request.args.get('type')]
    except KeyError:
        return {'message': 'Wrong `type` value'}, status.BAD_REQUEST

    scan = Scan.new(scan_type)
    scanner = Scanner(scan)
    scanner.perform()
    return '', status.OK


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
    try:
        save_settings(request.json)
    except Exception as error:
        print(error)
        return {'message': 'Bad JSON'}, status.BAD_REQUEST

    update_cameras()
    return '', status.OK


############


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('build/index.html')
