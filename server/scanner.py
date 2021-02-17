import logging
import cv2
import traceback
import sys
import storage

from datetime import datetime

from camera import Camera
from processing import undistort, project, compose
from custom_types import ImagesType, CamerasType, PathsType
from enums import CameraPosition, ImageLevel, ScanFile


cameras = {
    CameraPosition.RU: Camera('/dev/usb1', 'Canon', 'Canon Powershot S50'),
    CameraPosition.RL: Camera('/dev/usb2', 'Canon', 'Canon Powershot S50'),
    CameraPosition.LL: Camera('/dev/usb3', 'Nikon', 'Nikon Coolpix S9400'),
    CameraPosition.LU: Camera('/dev/usb4', 'Canon', 'Canon Powershot S50'),
}


def read_images(paths: PathsType):
    return {position: cv2.imread(paths[position]) for position in cameras}


def persist_image(path, image):
    cv2.imwrite(path, image)


def persist_images(paths: PathsType, images: ImagesType):
    for key in images:
        persist_image(paths[key], images[key])


class Scanner:
    def __init__(self, cameras: CamerasType = cameras, logger: logging.Logger = None):
        if cameras.keys() != CameraPosition.__members__.keys():
            raise ValueError('`cameras` dict keyword param must have all items from CameraPosition as keys')
        self.cameras = cameras

        self.logger = logger or logging.getLogger(__name__)
        self.setup_logger()

        self.scan_id = str(datetime.now().timestamp())
        self.paths = {level: storage.paths_for_image_level(self.scan_id, level) for level in ImageLevel}
        self.images = {level: dict.fromkeys(list(CameraPosition)) for level in ImageLevel}

        storage.create_scan_dir(self.scan_id)
        storage.copy_params_file(self.scan_id)

    def setup_logger(self):
        while self.logger.hasHandlers():
            self.logger.removeHandler(self.logger.handlers[0])

        log_file_path = storage.path_for_scan_file(self.scan_id, ScanFile.LOG)
        file_handler = logging.FileHandler(log_file_path)
        self.logger.addHandler(file_handler)

    def log(self, *args, **kwargs):
        if self.logger:
            self.logger.debug(*args, **kwargs)

    def capture_photos(self, paths: PathsType, cameras: CamerasType):
        for position, camera in cameras.items():
            self.log(f'Capture START, {position.value}, {repr(camera)}')
            camera.capture_to_path(paths[position])
            self.log(f'Capture END, {position.value}, {repr(camera)}')

    def build_undistorted_images(self, images: ImagesType, cameras: CamerasType):
        self.log('Building undistorted images...')
        return {position: undistort(images[position], cameras[position]) for position in cameras}

    def build_projected_images(self, images: ImagesType, cameras: CamerasType):
        self.log('Building projected images...')
        return {position: project(images[position], cameras[position]) for position in cameras}

    def build_result(self):
        self.log('Building result image...')
        return compose(self.images[ImageLevel.PROJECTED])

    def perform_scan(self):
        try:
            self.capture_photos(self.paths[ImageLevel.ORIGINAL], cameras)
            self.images[ImageLevel.ORIGINAL] = read_images(self.paths[ImageLevel.ORIGINAL])

            self.images[ImageLevel.UNDISTORTED] = self.build_undistorted_images(self.images[ImageLevel.ORIGINAL], cameras)
            persist_images(self.paths[ImageLevel.UNDISTORTED], self.images[ImageLevel.UNDISTORTED])

            self.images[ImageLevel.PROJECTED] = self.build_projected_images(self.images[ImageLevel.UNDISTORTED], cameras)
            persist_images(self.paths[ImageLevel.PROJECTED], self.images[ImageLevel.PROJECTED])

            result_image = self.build_result()
            result_image_path = storage.path_for_scan_file(self.scan_id, ScanFile.RESULT)
            persist_image(result_image_path, result_image)
        except Exception:
            self.log(f'Exception occurred\n\n{traceback.print_exception(*sys.exc_info())}')
            pass

    def perform_calibration(self):
        try:
            self.capture_photos(self.paths[ImageLevel.ORIGINAL], cameras)
            self.images[ImageLevel.ORIGINAL] = read_images(self.paths[ImageLevel.ORIGINAL])

            self.images[ImageLevel.UNDISTORTED] = self.build_undistorted_images(self.images[ImageLevel.ORIGINAL], cameras)
            persist_images(self.paths[ImageLevel.UNDISTORTED], self.images[ImageLevel.UNDISTORTED])
        except Exception:
            self.log(f'Exception occurred\n\n{traceback.print_exception(*sys.exc_info())}')
            pass