import gphoto2 as gp

from app_logger import logger
from settings import get_settings
from camera import DummyCamera, RealCamera, BlankCamera, CameraPosition


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
    if camera_data['type'] == 'real':
        serial_number = camera_data['serial_number']
        if serial_number not in mapping:
            raise KeyError(f'Could not detect camera with serial number {serial_number} (for position {position})')

        gp_camera = mapping[serial_number]
        return RealCamera(camera_data, gp_camera)
    elif camera_data['type'] == 'blank':
        return BlankCamera(camera_data, width=4896, height=3672)
    elif camera_data['type'] == 'dummy':
        return DummyCamera(camera_data, position)
    else:
        raise ValueError('Camera `type` must be one of "real", "blank", "dummy"')


def get_cameras():
    cameras_data = get_settings()['cameras']
    mapping = _get_gp_cameras_by_serial()

    cameras = {}

    for position, camera_data in cameras_data.items():
        position = CameraPosition[position]
        cameras[position] = _create_camera(camera_data, mapping, position)

    return cameras
