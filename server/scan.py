import os.path
import logging
import shutil
from enum import Enum
from datetime import datetime
from typing import Optional
from flask import url_for as flask_url_for

from cameras import CameraPosition
from server.constants.paths import SCANS_DIR_PATH, SETTINGS_FILE_PATH


DEFAULT_LOGGER = logging.getLogger(__name__)


class ScanType(Enum):
    SNAPSHOT = 'snapshot'
    CALIBRATION = 'calibration'


class Scan:
    def __init__(self, scan_type: ScanType, timestamp: Optional[str] = None, logger: logging.Logger = None, **kwargs):
        self.logger = logger or DEFAULT_LOGGER
        self.logger_handler = None

        self.type = scan_type
        self.timestamp = timestamp or str(int(datetime.now().timestamp()))

    @staticmethod
    def new(scan_type: ScanType):
        if scan_type == ScanType.SNAPSHOT:
            scan = SnapshotScan()
        elif scan_type == ScanType.CALIBRATION:
            scan = CalibrationScan()
        else:
            raise ValueError('Unknown (or None) scan_type value')

        os.mkdir(scan.root_directory)
        shutil.copy(SETTINGS_FILE_PATH, scan.root_directory)
        return scan

    @staticmethod
    def find_by_id(scan_id: str, *, check_existence=True):
        timestamp, scan_type = scan_id.split('_')
        scan = Scan(timestamp, ScanType[scan_type])

        if check_existence:
            if not os.path.exists(scan.root_directory):
                raise FileNotFoundError(f'Scan with id=`{scan_id}` does not exist')

        return scan

    @staticmethod
    def ids():
        return os.listdir(SCANS_DIR_PATH)

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


class SnapshotScan(Scan):
    def __init__(self, timestamp: Optional[str] = None, **kwargs):
        super().__init__(ScanType.SNAPSHOT, timestamp, **kwargs)

        self.images = {'result': None}
        self.paths = {'result': self.path_for('result')}
        self.urls = {'result': self.url_for('result')}

        for name in ['original', 'undistorted', 'projected']:
            self.images[name] = dict.fromkeys(CameraPosition)
            self.paths[name] = {self.path_for(name, position) for position in CameraPosition}
            self.urls[name] = {self.url_for(name, position) for position in CameraPosition}


class CalibrationScan(Scan):
    def __init__(self, timestamp: Optional[str] = None, **kwargs):
        super().__init__(ScanType.CALIBRATION, timestamp, **kwargs)

        self.images = {}
        self.paths = {}
        self.urls = {}

        for name in ['original', 'undistorted']:
            self.images[name] = dict.fromkeys(CameraPosition)
            self.paths[name] = {self.path_for(name, position) for position in CameraPosition}
            self.urls[name] = {self.url_for(name, position) for position in CameraPosition}
