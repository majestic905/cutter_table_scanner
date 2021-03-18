from threading import Thread
from app_logger import logger
from settings import get_settings
from processing import PathsType
from camera import Camera, CameraPosition


def _create_cameras():
    cameras_data = get_settings()['cameras']
    return {CameraPosition[key]: Camera(data) for key, data in cameras_data.items()}


_cameras = _create_cameras()


def update_cameras():
    global _cameras
    _cameras = _create_cameras()


def get_cameras():
    return _cameras


def _capture_photo(path: str, camera: Camera, position: str):
    logger.debug(f'Capture START, position: {position}')
    camera.capture_to_path(path)
    logger.debug(f'Capture   END, position: {position}')


def capture_photos(paths: PathsType):
    threads = {
        position: Thread(target=_capture_photo, args=(paths[position], _cameras[position], position.value))
        for position in CameraPosition
    }
    for position in CameraPosition:
        threads[position].start()
    for position in CameraPosition:
        threads[position].join()