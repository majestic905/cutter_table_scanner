from datetime import datetime
from http import HTTPStatus as status
from flask import request, send_from_directory

from app_logger import setup_logger, cleanup_logger
from settings import get_settings, save_settings, validate_settings
from cameras import update_cameras
from scan import Scan, ScanType
from app import app


@app.errorhandler(404)
def resource_not_found(e):
    return {"message": str(e)}, 404


@app.route('/api/scans', methods=['GET'])
def get_scans():
    scans = [
        {
            'scanId': scan.id,
            'scanType': scan.type.name,  # it's important to send .name, see Scan.find_by_id
            'createdAt': datetime.fromtimestamp(int(scan.timestamp)).strftime('%d %B %Y, %H:%M'),
            'images': scan.json_urls
        } for scan in Scan.all()
    ]

    return {'scans': list(reversed(scans))}


@app.route('/api/scans', methods=['POST'])
def post_scans():
    try:
        scan_type = ScanType[request.args.get('type')]
    except KeyError:
        return {'message': 'Wrong `type` value'}, status.BAD_REQUEST

    try:
        klass = scan_type.get_class()
        scan = klass()
        setup_logger(scan.log_file_path)
        scan.build()
    except Exception as error:
        return {'message': str(error)}, status.INTERNAL_SERVER_ERROR
    finally:
        cleanup_logger()

    return {'ok': True}, status.OK  # front-end checks for non-empty response


@app.route('/api/scans/<scan_id>/images/<filename>', methods=['GET'])
def get_scan_image(scan_id, filename):
    # TODO: this is a problem place which doesn't allow to easily put all thumb images into /thumbs/ subfolder
    directory = Scan.find(scan_id).root_directory
    return send_from_directory(directory, filename=filename, as_attachment=True)


@app.route('/api/scans', methods=['DELETE'])
def delete_scans():
    Scan.delete_all()
    return {'ok': True}, status.OK # front-end checks for non-empty response


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
