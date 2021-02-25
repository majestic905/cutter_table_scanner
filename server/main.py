from datetime import datetime
from http import HTTPStatus as status
from flask import request

from scan import Scan
from scanner import Scanner
from server.constants.enums import ScanFile, ScanType, ImageLevel
from app import app
from cameras import read_cameras_data, update_cameras_data



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
    scan = Scan.new(ScanType.SNAPSHOT)
    scanner = Scanner(scan)
    scanner.perform()
    return '', status.OK


@app.route('/api/scans', methods=['DELETE'])
def delete_scans():
    Scan.delete_all()
    return '', status.NO_CONTENT


@app.route('/api/cameras', methods=['GET'])
def get_cameras_data():
    return read_cameras_data()


@app.route('/api/cameras', methods=['POST'])
def post_cameras_data():
    update_cameras_data(request.json)
    return '', status.OK


# @app.route('/api/cameras/projection_points/calibrate', methods=['POST'])
# def camera_projection_points_calibrate():
#     scan = Scan.new(ScanType.CALIBRATION)
#     scanner = Scanner(scan)
#     scanner.perform()
#     return '', status.OK


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('build/index.html')
