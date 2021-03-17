import os.path
import logging
import shutil
import traceback
import sys
from enum import Enum
from datetime import datetime
from typing import Optional

from cameras import get_cameras
from processing import capture_photos, undistort, draw_polygons, project, compose
from image import FullImage, Grid, PathBuilder
from paths import SCANS_DIR_PATH, SETTINGS_FILE_PATH


DEFAULT_LOGGER = logging.getLogger(__name__)


class ScanType(Enum):
    SNAPSHOT = 'snapshot'
    CALIBRATION = 'calibration'

    def get_class(self):
        if self == ScanType.CALIBRATION:
            return CalibrationScan
        elif self == ScanType.SNAPSHOT:
            return SnapshotScan


class Scan:
    def __init__(self, scan_type: ScanType, timestamp: Optional[str] = None, logger: logging.Logger = None, **kwargs):
        self.logger = logger or DEFAULT_LOGGER
        self.logger_handler = None

        self.type = scan_type
        self.timestamp = timestamp or str(int(datetime.now().timestamp()))

        if timestamp is None:
            os.mkdir(self.root_directory)
            shutil.copy(SETTINGS_FILE_PATH, self.root_directory)

    def build(self):
        raise NotImplementedError

    @property
    def json_urls(self):
        raise NotImplementedError

    #########

    @staticmethod
    def all():
        for scan_id in os.listdir(SCANS_DIR_PATH):
            yield Scan.find(scan_id)

    @staticmethod
    def find(scan_id):
        timestamp, scan_type = scan_id.split('_')
        klass = ScanType[scan_type].get_class()
        return klass(timestamp)

    @staticmethod
    def delete_all():
        shutil.rmtree(SCANS_DIR_PATH)
        os.mkdir(SCANS_DIR_PATH)

    #########

    def log(self, *args, **kwargs):
        self.logger.debug(*args, **kwargs)

    def setup_logger(self):
        log_file_path = os.path.join(self.root_directory, 'log.txt')
        self.logger_handler = logging.FileHandler(log_file_path)
        self.logger.addHandler(self.logger_handler)

    def cleanup_logger(self):
        self.logger.removeHandler(self.logger_handler)
        self.logger_handler = None

    #########

    @property
    def id(self):
        return f'{self.timestamp}_{self.type.name}'

    @property
    def root_directory(self):
        return os.path.join(SCANS_DIR_PATH, self.id)


class SnapshotScan(Scan):
    def __init__(self, timestamp: Optional[str] = None, logger: logging.Logger = None, **kwargs):
        super().__init__(ScanType.SNAPSHOT, timestamp, logger, **kwargs)

        self.original = Grid('original')
        self.undistorted = Grid('undistorted')
        self.projected = Grid('projected')
        self.result = FullImage('result')

        self.path_builder = PathBuilder(self.id, self.root_directory)

    def build(self):
        cameras = get_cameras()

        try:
            self.setup_logger()

            original_images_paths = self.path_builder.paths_for(self.original, only='image')
            capture_photos(original_images_paths, cameras)
            self.original.read_from(original_images_paths)

            original_thumb_paths = self.path_builder.paths_for(self.original, only='thumb')
            self.original.persist_thumbnails_to(original_thumb_paths)

            undistorted_images = undistort(self.original.images, cameras)
            self.undistorted.images = draw_polygons(undistorted_images, cameras)
            undistorted_paths = self.path_builder.paths_for(self.undistorted)
            self.undistorted.persist_to(undistorted_paths)

            self.projected.images = project(undistorted_images, cameras)
            projected_paths = self.path_builder.paths_for(self.projected)
            self.projected.persist_to(projected_paths)

            self.result.image = compose(self.projected.images)
            result_path = self.path_builder.path_for(self.result)
            self.result.persist_to(result_path)
        except Exception:
            self.log(f'Exception occurred\n\n{traceback.print_exception(*sys.exc_info())}')
            raise
        finally:
            self.cleanup_logger()

    @property
    def json_urls(self):
        return {
            'original': self.path_builder.urls_for(self.original),
            'undistorted': self.path_builder.urls_for(self.undistorted),
            'projected': self.path_builder.urls_for(self.projected),
            'result': self.path_builder.url_for(self.result)
        }


class CalibrationScan(Scan):
    def __init__(self, timestamp: Optional[str] = None, logger: logging.Logger = None, **kwargs):
        super().__init__(ScanType.CALIBRATION, timestamp, logger, **kwargs)

        self.original = Grid('original')
        self.undistorted = Grid('undistorted')

        self.path_builder = PathBuilder(self.id, self.root_directory)

    def build(self):
        cameras = get_cameras()

        try:
            self.setup_logger()

            original_images_paths = self.path_builder.paths_for(self.original, only='image')
            capture_photos(original_images_paths, cameras)
            self.original.read_from(original_images_paths)

            original_thumb_paths = self.path_builder.paths_for(self.original, only='thumb')
            self.original.persist_thumbnails_to(original_thumb_paths)

            self.undistorted.images = undistort(self.original.images, cameras)
            undistorted_paths = self.path_builder.paths_for(self.undistorted)
            self.undistorted.persist_to(undistorted_paths)
        except Exception as error:
            self.log(f'Exception occurred\n\n{traceback.print_exception(*sys.exc_info())}')
            raise
        finally:
            self.cleanup_logger()

    @property
    def json_urls(self):
        return {
            'original': self.path_builder.urls_for(self.original),
            'undistorted': self.path_builder.urls_for(self.undistorted),
        }