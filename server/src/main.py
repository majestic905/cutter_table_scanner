import traceback
import json
from http import HTTPStatus as status
from flask import request

from app import app
from app.logger import read_log
from app.busy import acquire_busy_state, release_busy_state, check_is_busy
from processing.lensfun import read_lensfun_xml, save_lensfun_xml, validate_xml
from camera.data import get_cameras_data, save_cameras_data, validate_cameras_data
from scan import Scan
from scan.info import read_scan_info, write_scan_info



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
@check_is_busy
def build_scan():
    try:
        acquire_busy_state()
        scan_type = request.args.get('scan_type')
        use_lensfun = request.args.get('use_lensfun') == "true"
        scan_class = Scan.get_class(scan_type)
        scan = scan_class()
        scan.build(use_lensfun=use_lensfun)
    except Exception as error:
        traceback.print_exc()
        return {'message': str(error)}, status.INTERNAL_SERVER_ERROR
    finally:
        release_busy_state()

    return {'ok': True}, status.OK  # front-end checks for non-empty response


##############


@app.route('/api/cameras', methods=['GET'])
def send_cameras_data():
    cameras = {position.name: json.dumps(data, indent=4) for position, data in get_cameras_data().items()}
    return cameras


@app.route('/api/cameras', methods=['POST'])
@check_is_busy
def update_cameras_data():
    try:
        data = {position: json.loads(data) for position, data in request.json.items()}
    except json.JSONDecodeError as error:
        return {"message": str(error)}, status.BAD_REQUEST

    error_msg = validate_cameras_data(data)
    if error_msg is not None:
        return {"message": error_msg}, status.BAD_REQUEST

    save_cameras_data(data)
    return '', status.NO_CONTENT


##############


@app.route('/api/lensfun', methods=['GET'])
def send_lensfun_xml():
    return {'xml': read_lensfun_xml()}


@app.route('/api/lensfun', methods=['POST'])
@check_is_busy
def update_lensfun_xml():
    text = request.data.decode("utf-8")
    error_msg = validate_xml(text)

    if error_msg is not None:
        return {'message': error_msg}, status.BAD_REQUEST

    save_lensfun_xml(text)
    return '', status.NO_CONTENT


##############


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('front/index.html')


@app.errorhandler(404)
def resource_not_found(e):
    return {"message": str(e)}, 404