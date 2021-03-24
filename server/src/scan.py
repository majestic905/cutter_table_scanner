import shutil
from enum import Enum
from datetime import datetime
from typing import Optional
from pathlib import Path

from app_logger import logger
from cameras import get_cameras
from processing import capture_photos, disorient_images, flip_images, undistort, draw_polygons, project, compose
from image import FullImage, Grid, PathBuilder
from paths import SCANS_DIR_PATH, SETTINGS_FILE_PATH


class ScanType(Enum):
    SNAPSHOT = 'snapshot'
    CALIBRATION = 'calibration'

    def get_class(self):
        if self == ScanType.CALIBRATION:
            return CalibrationScan
        elif self == ScanType.SNAPSHOT:
            return SnapshotScan


class Scan:
    def __init__(self, scan_type: ScanType, timestamp: Optional[str] = None, **kwargs):
        self.type = scan_type
        self.timestamp = timestamp or str(int(datetime.now().timestamp()))

        if timestamp is None:
            self.root_directory.mkdir()
            shutil.copy(SETTINGS_FILE_PATH, self.root_directory)

    def build(self):
        raise NotImplementedError

    @property
    def json_urls(self):
        raise NotImplementedError

    #########

    @staticmethod
    def all():
        for scan_dir_path in SCANS_DIR_PATH.iterdir():
            yield Scan.find(scan_dir_path.name)

    @staticmethod
    def find(scan_id):
        timestamp, scan_type = scan_id.split('_')
        klass = ScanType[scan_type].get_class()
        return klass(timestamp)

    @staticmethod
    def delete_all():
        shutil.rmtree(SCANS_DIR_PATH)
        SCANS_DIR_PATH.mkdir()

    #########

    @property
    def id(self) -> str:
        return f'{self.timestamp}_{self.type.name}'

    @property
    def root_directory(self) -> Path:
        return SCANS_DIR_PATH / self.id

    @property
    def log_file_path(self) -> Path:
        return self.root_directory / 'log.txt'


class SnapshotScan(Scan):
    def __init__(self, timestamp: Optional[str] = None, **kwargs):
        super().__init__(ScanType.SNAPSHOT, timestamp, **kwargs)

        self.original = Grid('original')
        self.undistorted = Grid('undistorted')
        self.projected = Grid('projected')
        self.result = FullImage('result')

        self.path_builder = PathBuilder(self.id, self.root_directory)

    def build(self):
        cameras = get_cameras()

        try:
            original_images_paths = self.path_builder.paths_for(self.original, only='image')
            logger.info('Capturing photos...')
            capture_photos(original_images_paths, cameras)

            logger.info('Setting Exif.Image.Orientation=1 to disable undesired auto-rotation...')
            disorient_images(original_images_paths)

            original_thumb_paths = self.path_builder.paths_for(self.original, only='thumb')
            logger.info('Writing original photos thumbnails...')
            self.original.persist_thumbnails_to(original_thumb_paths)

            logger.info('Reading captured photos...')
            self.original.read_from(original_images_paths)

            logger.info('Flipping images vertically...')
            self.original = flip_images(self.original)

            logger.info('Undistorting original images...')
            undistorted_images = undistort(self.original.images, cameras)

            logger.info('Drawing polygons on undistorted images...')
            self.undistorted.images = draw_polygons(undistorted_images, cameras)

            undistorted_paths = self.path_builder.paths_for(self.undistorted)
            logger.info('Writing undistorted images with thumbnails...')
            self.undistorted.persist_to(undistorted_paths)

            logger.info('Projecting undistorted images...')
            self.projected.images = project(undistorted_images, cameras)

            projected_paths = self.path_builder.paths_for(self.projected)
            logger.info('Writing projected images with thumbnails...')
            self.projected.persist_to(projected_paths)

            logger.info('Composing result image...')
            self.result.image = compose(self.projected.images)

            result_path = self.path_builder.path_for(self.result)
            logger.info('Writing result image with thumbnail...')
            self.result.persist_to(result_path)
        except Exception:
            logger.exception(f'Unexpected error occurred...')
            raise

    @property
    def json_urls(self):
        return {
            'original': self.path_builder.urls_for(self.original),
            'undistorted': self.path_builder.urls_for(self.undistorted),
            'projected': self.path_builder.urls_for(self.projected),
            'result': self.path_builder.url_for(self.result)
        }


class CalibrationScan(Scan):
    def __init__(self, timestamp: Optional[str] = None, **kwargs):
        super().__init__(ScanType.CALIBRATION, timestamp, **kwargs)

        self.original = Grid('original')
        self.undistorted = Grid('undistorted')

        self.path_builder = PathBuilder(self.id, self.root_directory)

    def build(self):
        cameras = get_cameras()

        try:
            original_images_paths = self.path_builder.paths_for(self.original, only='image')
            logger.info('Capturing photos...')
            capture_photos(original_images_paths, cameras)

            logger.info('Setting Exif.Image.Orientation=1 to disable undesired auto-rotation...')
            disorient_images(original_images_paths)

            original_thumb_paths = self.path_builder.paths_for(self.original, only='thumb')
            logger.info('Writing original photos thumbnails...')
            self.original.persist_thumbnails_to(original_thumb_paths)

            logger.info('Reading photos...')
            self.original.read_from(original_images_paths)

            logger.info('Flipping images vertically...')
            self.original = flip_images(self.original)

            logger.info('Undistorting original images...')
            self.undistorted.images = undistort(self.original.images, cameras)

            undistorted_paths = self.path_builder.paths_for(self.undistorted)
            logger.info('Writing undistorted images with thumbnails...')
            self.undistorted.persist_to(undistorted_paths)
        except Exception as error:
            logger.exception(f'Unexpected error occurred...')
            raise

    @property
    def json_urls(self):
        return {
            'original': self.path_builder.urls_for(self.original),
            'undistorted': self.path_builder.urls_for(self.undistorted),
        }