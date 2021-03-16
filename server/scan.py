import os.path
import logging
import shutil
import traceback
import sys
from enum import Enum
from datetime import datetime
from typing import Optional
from flask import url_for as flask_url_for

from camera_position import CameraPosition
from cameras import get_cameras
from processing import capture_photos, read_images, persist_images, persist_image, undistort, draw_polygons,\
    project, compose, create_thumbnails, create_thumbnail
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

    #########

    @staticmethod
    def all():
        for scan_id in os.listdir(SCANS_DIR_PATH):
            timestamp, scan_type = scan_id.split('_')
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
        raise NotImplementedError


class SnapshotScan(Scan):
    def __init__(self, timestamp: Optional[str] = None, logger: logging.Logger = None, **kwargs):
        super().__init__(ScanType.SNAPSHOT, timestamp, logger, **kwargs)

        self.images = {'result': None}
        self.paths = {'result': self.path_for('result')}
        self.urls = {'result': self.url_for('result')}

        self.thumbs = {'result': None}
        self.thumb_paths = {'result': self.path_for('thumb_result')}
        self.thumb_urls = {'result': self.url_for('thumb_result')}

        for name in ['original', 'undistorted', 'projected']:
            self.images[name] = dict.fromkeys(CameraPosition)
            self.paths[name] = {position: self.path_for(name, position) for position in CameraPosition}
            self.urls[name] = {position: self.url_for(name, position) for position in CameraPosition}

            self.thumbs[name] = dict.fromkeys(CameraPosition)
            self.thumb_paths[name] = {position: self.path_for(f'thumb_{name}', position) for position in CameraPosition}
            self.thumb_urls[name] = {position: self.url_for(f'thumb_{name}', position) for position in CameraPosition}

    def build(self):
        cameras = get_cameras()

        try:
            self.setup_logger()
            paths, images = self.paths, self.images
            thumb_paths, thumbs = self.thumb_paths, self.thumbs

            capture_photos(paths['original'], cameras)

            images['original'] = read_images(paths['original'])
            undistorted = undistort(images['original'], cameras)
            images['undistorted'] = draw_polygons(undistorted, cameras)
            images['projected'] = project(undistorted, cameras)
            images['result'] = compose(images['projected'])

            persist_images(paths['undistorted'], images['undistorted'])
            persist_images(paths['projected'], images['projected'])
            persist_image(paths['result'], images['result'])

            thumbs['original'] = create_thumbnails(images['original'], 250)
            thumbs['undistorted'] = create_thumbnails(images['undistorted'], 250)
            thumbs['projected'] = create_thumbnails(images['projected'], 250)
            thumbs['result'] = create_thumbnail(images['result'], 500)

            persist_images(thumb_paths['original'], thumbs['original'])
            persist_images(thumb_paths['undistorted'], thumbs['undistorted'])
            persist_images(thumb_paths['projected'], thumbs['projected'])
            persist_image(thumb_paths['result'], thumbs['result'])
        except Exception:
            self.log(f'Exception occurred\n\n{traceback.print_exception(*sys.exc_info())}')
            raise
        finally:
            self.cleanup_logger()

    @property
    def json_urls(self):
        urls = {}
        for name in ['original', 'undistorted', 'projected']:
            urls[name] = {position.name: None for position in CameraPosition}
            for position in CameraPosition:
                urls[name][position.name] = {
                    'full': self.urls[name][position],
                    'thumb': self.thumb_urls[name][position]
                }
        urls['result'] = {
            'full': self.urls['result'],
            'thumb': self.thumb_urls['result']
        }
        return urls


class CalibrationScan(Scan):
    def __init__(self, timestamp: Optional[str] = None, logger: logging.Logger = None, **kwargs):
        super().__init__(ScanType.CALIBRATION, timestamp, logger, **kwargs)

        self.images = {}
        self.paths = {}
        self.urls = {}

        self.thumbs = {}
        self.thumb_paths = {}
        self.thumb_urls = {}

        for name in ['original', 'undistorted']:
            self.images[name] = dict.fromkeys(CameraPosition)
            self.paths[name] = {position: self.path_for(name, position) for position in CameraPosition}
            self.urls[name] = {position: self.url_for(name, position) for position in CameraPosition}

            self.thumbs[name] = dict.fromkeys(CameraPosition)
            self.thumb_paths[name] = {position: self.path_for(f'thumb_{name}', position) for position in CameraPosition}
            self.thumb_urls[name] = {position: self.url_for(f'thumb_{name}', position) for position in CameraPosition}

    def build(self):
        cameras = get_cameras()

        try:
            self.setup_logger()
            paths, images = self.paths, self.images
            thumb_paths, thumbs = self.thumb_paths, self.thumbs

            capture_photos(paths['original'], cameras)

            images['original'] = read_images(paths['original'])
            images['undistorted'] = undistort(images['original'], cameras)

            persist_images(paths['undistorted'], images['undistorted'])

            thumbs['original'] = create_thumbnails(images['original'], 250)
            thumbs['undistorted'] = create_thumbnails(images['undistorted'], 250)

            persist_images(thumb_paths['original'], thumbs['original'])
            persist_images(thumb_paths['undistorted'], thumbs['undistorted'])
        except Exception as error:
            self.log(f'Exception occurred\n\n{traceback.print_exception(*sys.exc_info())}')
            raise
        finally:
            self.cleanup_logger()

    @property
    def json_urls(self):
        urls = {}
        for name in ['original', 'undistorted']:
            urls[name] = {position.name: None for position in CameraPosition}
            for position in CameraPosition:
                urls[name][position.name] = {
                    'full': self.urls[name][position],
                    'thumb': self.thumb_urls[name][position]
                }
        return urls