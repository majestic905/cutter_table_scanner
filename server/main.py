import os.path
from scan import Scan
from scanner import Scanner
from server.constants.enums import ScanFile, ScanType, ImageLevel
from datetime import datetime

from http import HTTPStatus as status
from flask import send_from_directory, request
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

        images = {level: scan.paths_for_image_level(level) for level in image_levels}
        for image_level in images:
            item['images'][image_level.name] = {}
            for camera_position in images[image_level]:
                item['images'][image_level.name][camera_position.name] = images[image_level][camera_position]

        if scan.type == ScanType.SNAPSHOT:
            item['images'][ScanFile.RESULT.name] = scan.path_for(ScanFile.RESULT)

        scans.append(item)

    return {'scans': scans}


@app.route('/api/scans/<scan_id>', methods=['GET'])
def get_scan(scan_id):
    scan = Scan.find_by_id(scan_id)
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


# @app.route('/api/cameras/projection_points/calibrate', methods=['POST'])
# def camera_projection_points_calibrate():
#     scan = Scan.new(ScanType.CALIBRATION)
#     scanner = Scanner(scan)
#     scanner.make_calibration_images()
#     return '', status.OK


# @app.route('/api/cameras/projection_points', methods=['POST'])
# def camera_projection_points_set():
#     scanner = Scanner()
#     scanner.perform_calibration()
#     return '', status.OK


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('build/index.html')
