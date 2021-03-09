import os.path
import logging
import shutil
import numpy as np
from datetime import datetime
from typing import Optional
from flask import url_for as flask_url_for

from server.constants.paths import SCANS_DIR_PATH, SETTINGS_FILE_PATH
from server.constants.enums import ScanType, ScanFile, ImageLevel, CameraPosition


DEFAULT_LOGGER = logging.getLogger(__name__)


class Scan:
    def __init__(self, timestamp: Optional[str], scan_type: ScanType, logger: logging.Logger = None, **kwargs):
        self.timestamp = timestamp or str(int(datetime.now().timestamp()))
        self.type = scan_type

        self.logger = logger or DEFAULT_LOGGER
        self.logger_handler = None

    @staticmethod
    def new(scan_type: ScanType):
        scan = Scan(None, scan_type)
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

    def url_for(self, scan_file: ScanFile):
        return flask_url_for('static', filename=f'data/scans/{self.id}/{scan_file.value}')

    def urls_for_image_level(self, level: ImageLevel):
        return {position: self.url_for(ScanFile.image(position, level)) for position in CameraPosition}

    #########

    @staticmethod
    def ids():
        return os.listdir(SCANS_DIR_PATH)

    @staticmethod
    def delete_all():
        shutil.rmtree(SCANS_DIR_PATH)
        os.mkdir(SCANS_DIR_PATH)


class Images:
    def __init__(self, name):
        self.name = name
        self.images = dict.fromkeys(CameraPosition)

    def filename_for(self, position: CameraPosition):
        return f'{position.value}_{self.name}.jpg'

    def __getitem__(self, position: CameraPosition):
        return self.images[position]

    def __setitem__(self, position: CameraPosition, image: np.ndarray):
        self.images[position] = image



class SnapshotScan(Scan):
    def __init__(self, timestamp: Optional[str], scan_type: ScanType, *args, **kwargs):
        super().__init__(timestamp, scan_type, **kwargs)

        self.images = {'result': None}
        self.paths = {'result': os.path.join(self.root_directory, 'result.jog')}

        for name in ['original', 'undistorted', 'projected']:
            self.images[name] = dict.fromkeys(CameraPosition)
            self.paths[name] = {self.path_for(name, position) for position in CameraPosition}

    def image_filename_for(self, name: str, position: CameraPosition = None):
        return 'result.jpg' if position is None else f'{position.value}_{name}.jpg'

    def path_for(self, name: str, position: CameraPosition):
        return os.path.join(self.root_directory, self.image_filename_for(name, position))

    def url_for(self, scan_file: ScanFile):
        return flask_url_for('static', filename=f'data/scans/{self.id}/{scan_file.value}')


class CalibrationScan(Scan):
    def __init__(self, timestamp: Optional[str], scan_type: ScanType, *args, **kwargs):
        super().__init__(timestamp, scan_type, **kwargs)

        self.images, self.paths = {}, {}
        for name in ['original', 'undistorted']:
            self.images[name] = dict.fromkeys(CameraPosition)
            self.paths[name] = {self.path_for(position, name) for position in CameraPosition}

    def path_for(self, position: CameraPosition, name: str):
        return os.path.join(self.root_directory, f'{position.value}_{name}.jpg')