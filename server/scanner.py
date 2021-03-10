import traceback
import sys
import cv2

from settings import get_settings
from cameras import get_cameras
from scan import SnapshotScan, CalibrationScan
from processing import undistort, project, compose
from server.constants.custom_types import ImagesType, CamerasType, PathsType, ExifType


def read_images(paths: PathsType):
    return {position: cv2.imread(paths[position]) for position in paths}


def persist_image(path, image):
    cv2.imwrite(path, image)


def persist_images(paths: PathsType, images: ImagesType):
    for key in images:
        persist_image(paths[key], images[key])


def capture_photos(paths: PathsType, cameras: CamerasType):
    for position, camera in cameras.items():
        # scan.log(f'Capture START, {position.value}, {repr(camera)}')
        camera.capture_to_path(paths[position])
        # scan.log(f'Capture END, {position.value}, {repr(camera)}')


def build_undistorted_images(images: ImagesType, cameras: CamerasType):
    # scan.log('Building undistorted images...')
    return {position: undistort(images[position], cameras[position]) for position in cameras}


def build_projected_images(images: ImagesType, cameras: CamerasType):
    # scan.log('Building projected images...')
    image_sizes = get_settings()['image_sizes']

    return {
        position: project(images[position], cameras[position], image_sizes[position.name])
        for position in cameras
    }


def build_result(images: ImagesType):
    # scan.log('Building result image...')
    return compose(images)


def build_snapshot():
    scan = SnapshotScan()
    cameras = get_cameras()

    try:
        scan.setup_logger()
        paths, images = scan.paths, scan.images

        capture_photos(paths['original'], cameras)

        images['original'] = read_images(paths['original'])
        images['undistorted'] = build_undistorted_images(images['original'], cameras)
        images['projected'] = build_projected_images(images['undistorted'], cameras)
        images['result'] = build_result(images['projected'])

        persist_images(paths['undistorted'], images['undistorted'])
        persist_images(paths['projected'], images['projected'])
        persist_image(paths['result'], images['result'])
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

        capture_photos(paths['original'], cameras)

        images['original'] = read_images(paths['original'])
        images['undistorted'] = build_undistorted_images(images['original'], cameras)

        persist_images(paths['undistorted'], images['undistorted'])
    except Exception:
        scan.log(f'Exception occurred\n\n{traceback.print_exception(*sys.exc_info())}')
    finally:
        scan.cleanup_logger()
