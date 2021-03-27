import traceback
from http import HTTPStatus as status
from flask import request

from app import app
from app_logger import read_log, clear_log
from settings import get_settings, save_settings, validate_settings
from scan import Scan
from scan_info import read_scan_info, write_scan_info



@app.errorhandler(404)
def resource_not_found(e):
    return {"message": str(e)}, 404



@app.route('/api/scan', methods=['GET'])
def send_scan():
    info = read_scan_info()
    scan_type, created_at = info['scan_type'], info['created_at']

    response = {
        'scanType': info['scan_type'],
        'createdAt': info['created_at'],
        'log': read_log()
    }

    try:
        response['images'] = Scan.get_class(scan_type)().json_urls
    except ValueError:
        pass

    return response


@app.route('/api/scan', methods=['POST'])
def build_scan():
    scan_type = request.args.get('type')

    try:
        scan_class = Scan.get_class(scan_type)
        write_scan_info(scan_type)
        clear_log()
        scan = scan_class()
        scan.build()
    except Exception as error:
        traceback.print_exc()
        return {'message': str(error)}, status.INTERNAL_SERVER_ERROR

    return {'ok': True}, status.OK  # front-end checks for non-empty response



@app.route('/api/settings', methods=['GET'])
def send_settings():
    return get_settings()


@app.route('/api/settings', methods=['POST'])
def update_settings():
    error_msg = validate_settings(request.json)
    if error_msg is not None:
        return {'message': error_msg}, status.BAD_REQUEST

    save_settings(request.json)
    return '', status.NO_CONTENT



@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('build/index.html')
