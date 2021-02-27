import traceback
import sys
import os.path
import cv2
from pyexiv2 import Image

from scan import Scan
from cameras import cameras
from processing import undistort, project, compose
from server.constants.custom_types import ImagesType, CamerasType, PathsType, ExifType
from server.constants.enums import CameraPosition, ImageLevel, ScanFile, ScanType


def read_images(paths: PathsType):
    return {position: cv2.imread(paths[position]) for position in paths}


def persist_image(path, image):
    cv2.imwrite(path, image)


def persist_images(paths: PathsType, images: ImagesType):
    for key in images:
        persist_image(paths[key], images[key])


def read_exif_data(paths: PathsType):
    exif_data = {}

    for position, file_path in paths.items():
        with Image(file_path) as img:
            data = img.read_exif()
            exif_data[position] = {
                'focal_length': eval(data['Exif.Photo.FocalLength']),  # eval('3520/1000')
                'aperture': eval(data['Exif.Photo.FNumber'])  # eval('180/100')
            }

    return exif_data


class Scanner:
    def __init__(self, scan: Scan, cameras: CamerasType = cameras):
        self.scan = scan
        self.cameras = cameras

        if set(cameras.keys()) != set(CameraPosition):
            raise ValueError('`cameras` dict must have all items from CameraPosition as keys')

    def log(self, *args, **kwargs):
        self.scan.log(*args, **kwargs)

    def capture_photos(self, paths: PathsType, cameras: CamerasType):
        for position, camera in cameras.items():
            self.log(f'Capture START, {position.value}, {repr(camera)}')
            camera.capture_to_path(paths[position])
            self.log(f'Capture END, {position.value}, {repr(camera)}')

    def build_undistorted_images(self, images: ImagesType, exif: ExifType, cameras: CamerasType):
        self.log('Building undistorted images...')
        return {position: undistort(images[position], exif[position], cameras[position]) for position in cameras}

    def build_projected_images(self, images: ImagesType, cameras: CamerasType):
        self.log('Building projected images...')
        return {position: project(images[position], cameras[position]) for position in cameras}

    def build_result(self, images: ImagesType):
        self.log('Building result image...')

        src_path = os.path.join(__file__, '..', 'eggs', 'sample_scan', ScanFile.RESULT.value)
        return cv2.imread(src_path)

        # return compose(images)

    def make_snapshot(self):
        try:
            self.scan.setup_logger()
            paths, images = self.scan.paths, self.scan.images

            self.capture_photos(paths[ImageLevel.ORIGINAL], cameras)
            images[ImageLevel.ORIGINAL] = read_images(paths[ImageLevel.ORIGINAL])

            exif = read_exif_data(paths[ImageLevel.ORIGINAL])
            images[ImageLevel.UNDISTORTED] = self.build_undistorted_images(images[ImageLevel.ORIGINAL], exif, cameras)
            persist_images(paths[ImageLevel.UNDISTORTED], images[ImageLevel.UNDISTORTED])

            images[ImageLevel.PROJECTED] = self.build_projected_images(images[ImageLevel.UNDISTORTED], cameras)
            persist_images(paths[ImageLevel.PROJECTED], images[ImageLevel.PROJECTED])

            result_image = self.build_result(images[ImageLevel.PROJECTED])
            result_image_path = self.scan.path_for(ScanFile.RESULT)
            persist_image(result_image_path, result_image)
        except Exception:
            self.log(f'Exception occurred\n\n{traceback.print_exception(*sys.exc_info())}')
        finally:
            self.scan.cleanup_logger()

    def make_calibration_images(self):
        try:
            self.scan.setup_logger()
            paths, images = self.scan.paths, self.scan.images

            self.capture_photos(paths[ImageLevel.ORIGINAL], cameras)
            images[ImageLevel.ORIGINAL] = read_images(paths[ImageLevel.ORIGINAL])

            images[ImageLevel.UNDISTORTED] = self.build_undistorted_images(images[ImageLevel.ORIGINAL], cameras)
            persist_images(paths[ImageLevel.UNDISTORTED], images[ImageLevel.UNDISTORTED])
        except Exception:
            self.log(f'Exception occurred\n\n{traceback.print_exception(*sys.exc_info())}')
        finally:
            self.scan.cleanup_logger()

    def perform(self):
        if self.scan.type == ScanType.SNAPSHOT:
            self.make_snapshot()
        elif self.scan.type == ScanType.CALIBRATION:
            self.make_calibration_images()