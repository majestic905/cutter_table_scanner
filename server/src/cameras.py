import gphoto2 as gp

from app import app
from app_logger import logger
from cameras_data import get_cameras_data
from camera import DummyCamera, RealCamera, CameraPosition


def _get_gp_cameras_by_serial():
    port_info_list = gp.PortInfoList()
    port_info_list.load()

    def get_port_info(addr):
        index = port_info_list.lookup_path(addr)
        return port_info_list[index]

    def get_camera(name, addr):
        camera = gp.Camera()
        camera.set_port_info(get_port_info(addr))
        camera.init()

        serial_number = camera.get_single_config('serialnumber').get_value()
        logger.debug(f'Port {addr} is taken by camera with name `{name}` and serial number `{serial_number}`')
        return serial_number, camera

    return dict([get_camera(name, addr) for name, addr in gp.Camera.autodetect()])


def _create_camera(camera_data: dict, mapping: dict, position: CameraPosition):
    serial_number = camera_data['serial_number']

    if serial_number not in mapping:
        raise KeyError(f'Could not detect camera with serial number {serial_number} (for position {position})')

    return RealCamera(camera_data, mapping[serial_number])


def _get_cameras_production():
    mapping = _get_gp_cameras_by_serial()
    cameras_data = get_cameras_data()
    cameras_data = {CameraPosition[position]: camera_data for position, camera_data in cameras_data.items()}
    return {position: _create_camera(camera_data, mapping, position) for position, camera_data in cameras_data.items()}


def _get_cameras_development():
    cameras_data = get_cameras_data()
    cameras_data = {CameraPosition[position]: camera_data for position, camera_data in cameras_data.items()}
    return {position: DummyCamera(camera_data, position) for position, camera_data in cameras_data.items()}


def get_cameras():
    if app.env == "development":
        return _get_cameras_development()
    else:
        return _get_cameras_production()