import os.path
import logging
import shutil
from datetime import datetime
from typing import Optional
from flask import url_for as flask_url_for

from server.constants.paths import SCANS_DIR_PATH, CAMERAS_FILE_PATH
from server.constants.enums import ScanType, ScanFile, ImageLevel, CameraPosition


DEFAULT_LOGGER = logging.getLogger(__name__)


class Scan:
    def __init__(self, timestamp: Optional[str], scan_type: ScanType, logger: logging.Logger = None, **kwargs):
        self.timestamp = timestamp or str(int(datetime.now().timestamp()))
        self.type = scan_type

        self.logger = logger or DEFAULT_LOGGER
        self.logger_handler = None

        self.paths = {level: self.paths_for_image_level(level) for level in ImageLevel}
        self.images = {level: dict.fromkeys(list(CameraPosition)) for level in ImageLevel}

    @staticmethod
    def new(scan_type: ScanType):
        scan = Scan(None, scan_type)
        os.mkdir(scan.root_directory)
        shutil.copy(CAMERAS_FILE_PATH, scan.path_for(ScanFile.CAMERAS))
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
        log_file_path = self.path_for(ScanFile.LOG)
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

    def path_for(self, scan_file: ScanFile):
        return os.path.join(self.root_directory, scan_file.value)

    def paths_for_image_level(self, level: ImageLevel):
        return {position: self.path_for(ScanFile.image(position, level)) for position in CameraPosition}

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
