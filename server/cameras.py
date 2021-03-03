import settings
from camera import Camera
from server.constants.enums import CameraPosition


def _create_camera(data: dict):
    projection_points = {CameraPosition[key]: value for key, value in data['projection_points'].items()}
    return Camera(data['usb_port'], data['maker'], data['model'], projection_points=projection_points)


def _create_cameras():
    cameras_data = settings.get_settings()['cameras']
    return {CameraPosition[key]: _create_camera(data) for key, data in cameras_data.items()}


def update_cameras():
    global _cameras
    _cameras = _create_cameras()


def get_cameras():
    return _cameras


_cameras = _create_cameras()