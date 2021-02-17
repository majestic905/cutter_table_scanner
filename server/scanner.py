import logging
import cv2
import traceback
import sys
import storage

from scan import Scan
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
    def __init__(self, scan: Scan, cameras: CamerasType = cameras):
        self.scan = scan
        self.cameras = cameras

        if cameras.keys() != CameraPosition.__members__.keys():
            raise ValueError('`cameras` dict must have all items from CameraPosition as keys')

    def log(self, *args, **kwargs):
        self.scan.log(*args, **kwargs)

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

    def build_result(self, images: ImagesType):
        self.log('Building result image...')
        return compose(images)

    def snapshot_to(self, scan: Scan):
        try:
            scan.setup_logger()
            paths, images = scan.paths, scan.images

            self.capture_photos(paths[ImageLevel.ORIGINAL], cameras)
            images[ImageLevel.ORIGINAL] = read_images(paths[ImageLevel.ORIGINAL])

            images[ImageLevel.UNDISTORTED] = self.build_undistorted_images(images[ImageLevel.ORIGINAL], cameras)
            persist_images(paths[ImageLevel.UNDISTORTED], images[ImageLevel.UNDISTORTED])

            images[ImageLevel.PROJECTED] = self.build_projected_images(images[ImageLevel.UNDISTORTED], cameras)
            persist_images(paths[ImageLevel.PROJECTED], images[ImageLevel.PROJECTED])

            result_image = self.build_result(images[ImageLevel.PROJECTED])
            result_image_path = scan.path_for(ScanFile.RESULT)
            persist_image(result_image_path, result_image)
        except Exception:
            self.log(f'Exception occurred\n\n{traceback.print_exception(*sys.exc_info())}')
            pass
        finally:
            scan.cleanup_logger()

    def calibrate_to(self, scan: ScanFile):
        try:
            scan.setup_logger()
            paths, images = scan.paths, scan.images

            self.capture_photos(paths[ImageLevel.ORIGINAL], cameras)
            images[ImageLevel.ORIGINAL] = read_images(paths[ImageLevel.ORIGINAL])

            images[ImageLevel.UNDISTORTED] = self.build_undistorted_images(images[ImageLevel.ORIGINAL], cameras)
            persist_images(paths[ImageLevel.UNDISTORTED], images[ImageLevel.UNDISTORTED])
        except Exception:
            self.log(f'Exception occurred\n\n{traceback.print_exception(*sys.exc_info())}')
            pass
        finally:
            scan.cleanup_logger()