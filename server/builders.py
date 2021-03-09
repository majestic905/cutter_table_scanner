import traceback
import sys
import cv2
from cameras import get_cameras
from server.constants.custom_types import PathsType, CamerasType, ImagesType
from processing import undistort, project, compose


def _read_images(paths: PathsType):
    return {position: cv2.imread(paths[position]) for position in paths}


def _persist_image(path, image):
    cv2.imwrite(path, image)


def _persist_images(paths: PathsType, images: ImagesType):
    for position in images:
        _persist_image(paths[position], images[position])


def _capture_photos(paths: PathsType, cameras: CamerasType):
    for position, camera in cameras.items():
        # logging.debug(f'Capture START, {position.value}, {repr(camera)}')
        camera.capture_to_path(paths[position])
        # logging.debug(f'Capture END, {position.value}, {repr(camera)}')


def _build_undistorted_images(images: ImagesType, cameras: CamerasType):
    # logging.debug('Building undistorted images...')
    return {position: undistort(images[position], cameras[position]) for position in cameras}


def _build_projected_images(images: ImagesType, cameras: CamerasType):
    # logging.debug('Building projected images...')
    return {position: project(images[position], cameras[position]) for position in cameras}


def _resize_images(cameras: CamerasType, image_sizes):
    pass


def _build_result(images: ImagesType, cameras: CamerasType):
    # logging.debug('Building result image...')
    return compose(images)


def build_snapshot():
    scan = SnapshotScan()
    cameras = get_cameras()

    try:
        scan.setup_logger()
        paths, images = scan.paths, scan.images

        _capture_photos(paths['original'], cameras)

        images['original'] = _read_images(paths['original'])
        images['undistorted'] = _build_undistorted_images(images['original'], cameras)
        images['projected'] = _build_projected_images(images['undistorted'], cameras)
        images['result'] = _build_result(images['projected'], cameras)

        _persist_images(paths['undistorted'], images['undistorted'])
        _persist_images(paths['projected'], images['projected'])
        _persist_image(paths['result'], images['result'])
    except Exception:
        scan.log(f'Exception occurred\n\n{traceback.print_exception(*sys.exc_info())}')
    finally:
        scan.cleanup_logger()


def build_calibration():
    scan = CalibrationScan()
    cameras = get_cameras()

    try:
        scan.setup_logger()
        paths, images = scan.paths, scan.images

        _capture_photos(paths['original'], cameras)

        images['original'] = _read_images(paths['original'])
        images['undistorted'] = _build_undistorted_images(images['original'], cameras)
        images['projected'] = _build_projected_images(images['undistorted'], cameras)
        images['result'] = _build_result(images['projected'], cameras)

        _persist_images(paths['undistorted'], images['undistorted'])
        _persist_images(paths['projected'], images['projected'])
        _persist_image(paths['result'], images['result'])
    except Exception:
        scan.log(f'Exception occurred\n\n{traceback.print_exception(*sys.exc_info())}')
    finally:
        scan.cleanup_logger()


class SnapshotScan:
    def __init__(self):
        self.paths = {level: self.paths_for_image_level(level) for level in ImageLevel}
        self.images = {level: dict.fromkeys(CameraPosition) for level in ImageLevel}

    def setup_logger(self):
        pass

    def cleanup_logger(self):
        pass


class CalibrationScan:
    pass