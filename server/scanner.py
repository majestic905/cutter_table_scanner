import logging
import cv2
import numpy as np

import storage

from typing import Dict
from datetime import datetime

from storage import ScanFile, ImageLevel
from camera import Camera, CameraPosition
from processing import undistort, project, compose


ImagesType = Dict[CameraPosition, np.ndarray]
CamerasType = Dict[CameraPosition, Camera]
PathsType = Dict[CameraPosition, str]


logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


cameras = {
    CameraPosition.RU: Camera('/dev/usb1', 'Canon', 'Canon Powershot S50'),
    CameraPosition.RL: Camera('/dev/usb2', 'Canon', 'Canon Powershot S50'),
    CameraPosition.LL: Camera('/dev/usb3', 'Nikon', 'Nikon Coolpix S9400'),
    CameraPosition.LU: Camera('/dev/usb4', 'Canon', 'Canon Powershot S50'),
}


def capture_photos(paths: PathsType, cameras: CamerasType):
    for position, camera in cameras.items():
        camera.capture_to_path(paths[position])


def build_undistorted_images(images: ImagesType, cameras: CamerasType):
    return {position: undistort(images[position], cameras[position]) for position in cameras}


def build_projected_images(images: ImagesType, cameras: CamerasType):
    return {position: project(images[position], cameras[position]) for position in cameras}


def read_images(paths: PathsType):
    return {position: cv2.imread(paths[position]) for position in cameras}


def persist_image(path, image):
    cv2.imwrite(path, image)


def persist_images(paths: PathsType, images: ImagesType):
    for key in images:
        persist_image(paths[key], images[key])
        cv2.imwrite(paths[key], images[key])


def perform_scan():
    scan_id = str(datetime.now().timestamp())

    storage.create_scan_dir(scan_id)
    storage.copy_params_file(scan_id)

    log_file_path = storage.path_for_scan_file(scan_id, ScanFile.LOG)
    logger_file_handler = logging.FileHandler(log_file_path)
    logger.addHandler(logger_file_handler)

    paths = {level: storage.paths_for_image_level(scan_id, level) for level in ImageLevel}
    images = {level: dict.fromkeys(list(CameraPosition)) for level in ImageLevel}

    try:
        capture_photos(paths[ImageLevel.ORIGINAL], cameras)
        images[ImageLevel.ORIGINAL] = read_images(paths[ImageLevel.ORIGINAL])

        images[ImageLevel.UNDISTORTED] = build_undistorted_images(images[ImageLevel.ORIGINAL], cameras)
        persist_images(paths[ImageLevel.UNDISTORTED], images[ImageLevel.UNDISTORTED])

        images[ImageLevel.PROJECTED] = build_projected_images(images[ImageLevel.UNDISTORTED], cameras)
        persist_images(paths[ImageLevel.PROJECTED], images[ImageLevel.PROJECTED])

        result_image = compose(images[ImageLevel.PROJECTED])
        result_image_path = storage.path_for_scan_file(scan_id, ScanFile.RESULT)
        persist_image(result_image_path, result_image)
    except Exception:
        # log exception
        pass
    finally:
        logger.removeHandler(logger_file_handler)