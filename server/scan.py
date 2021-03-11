import os.path
import logging
import shutil
import traceback
import sys
from enum import Enum
from datetime import datetime
from typing import Optional
from flask import url_for as flask_url_for

from cameras import CameraPosition, get_cameras
from processing import capture_photos, read_images, persist_images, persist_image, undistort, project, compose
from server.constants.paths import SCANS_DIR_PATH, SETTINGS_FILE_PATH


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

    #########

    @staticmethod
    def all():
        for scan_id in os.listdir(SCANS_DIR_PATH):
            timestamp, scan_type = scan_id.split('_')
            # print(scan_type, ScanType[scan_type], ScanType[scan_type].get_class())
            klass = ScanType[scan_type].get_class()
            yield klass(timestamp)

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

    #########

    def image_filename_for(self, name: str, position: CameraPosition = None):
        return f'{name}.jpg' if position is None else f'{position.value}_{name}.jpg'

    def path_for(self, name: str, position: CameraPosition = None):
        filename = self.image_filename_for(name, position)
        return os.path.join(self.root_directory, filename)

    def url_for(self, name: str, position: CameraPosition = None):
        filename = self.image_filename_for(name, position)
        return flask_url_for('static', filename=f'data/scans/{self.id}/{filename}')

    @property
    def json_urls(self):
        result = {}
        for name, value in self.urls.items():
            result[name] = value
            if isinstance(value, dict):
                result[name] = {position.name: url for position, url in value.items()}
        return result


class SnapshotScan(Scan):
    def __init__(self, timestamp: Optional[str] = None, logger: logging.Logger = None, **kwargs):
        super().__init__(ScanType.SNAPSHOT, timestamp, logger, **kwargs)

        self.images = {'result': None}
        self.paths = {'result': self.path_for('result')}
        self.urls = {'result': self.url_for('result')}

        for name in ['original', 'undistorted', 'projected']:
            self.images[name] = dict.fromkeys(CameraPosition)
            self.paths[name] = {position: self.path_for(name, position) for position in CameraPosition}
            self.urls[name] = {position: self.url_for(name, position) for position in CameraPosition}

    def build(self):
        cameras = get_cameras()

        try:
            self.setup_logger()
            paths, images = self.paths, self.images

            capture_photos(paths['original'], cameras)

            images['original'] = read_images(paths['original'])
            images['undistorted'] = undistort(images['original'], cameras)
            images['projected'] = project(images['undistorted'], cameras)
            images['result'] = compose(images['projected'])

            persist_images(paths['undistorted'], images['undistorted'])
            persist_images(paths['projected'], images['projected'])
            persist_image(paths['result'], images['result'])
        except Exception:
            self.log(f'Exception occurred\n\n{traceback.print_exception(*sys.exc_info())}')
        finally:
            self.cleanup_logger()


class CalibrationScan(Scan):
    def __init__(self, timestamp: Optional[str] = None, logger: logging.Logger = None, **kwargs):
        super().__init__(ScanType.CALIBRATION, timestamp, logger, **kwargs)

        self.images = {}
        self.paths = {}
        self.urls = {}

        for name in ['original', 'undistorted']:
            self.images[name] = dict.fromkeys(CameraPosition)
            self.paths[name] = {position: self.path_for(name, position) for position in CameraPosition}
            self.urls[name] = {position: self.url_for(name, position) for position in CameraPosition}

    def build(self):
        cameras = get_cameras()

        try:
            self.setup_logger()
            paths, images = self.paths, self.images

            capture_photos(paths['original'], cameras)

            images['original'] = read_images(paths['original'])
            images['undistorted'] = undistort(images['original'], cameras)

            persist_images(paths['undistorted'], images['undistorted'])
        except Exception:
            self.log(f'Exception occurred\n\n{traceback.print_exception(*sys.exc_info())}')
        finally:
            self.cleanup_logger()