import storage
import logging
from enums import ScanType, ScanFile, ImageLevel, CameraPosition

from datetime import datetime


DEFAULT_LOGGER = logging.getLogger(__name__)


class Scan:
    def __init__(self, scan_type: ScanType, logger: logging.Logger = None):
        self.id = str(datetime.now().timestamp())
        self.type = scan_type

        self.logger = logger or DEFAULT_LOGGER
        self.logger_handler = None

        self.paths = {level: storage.paths_for_image_level(self.id, level) for level in ImageLevel}
        self.images = {level: dict.fromkeys(list(CameraPosition)) for level in ImageLevel}

        storage.create_scan_dir(self.id, self.type)
        storage.copy_params_file(self.id, self.type)

    def setup_logger(self):
        log_file_path = self.path_for(ScanFile.LOG)
        self.logger_handler = logging.FileHandler(log_file_path)
        self.logger.addHandler(self.logger_handler)

    def cleanup_logger(self):
        self.logger.removeHandler(self.logger_handler)
        self.logger_handler = None

    def path_for(self, scan_file: ScanFile):
        return storage.path_for_scan_file(self.id, self.type, scan_file)

    def log(self, *args, **kwargs):
        self.logger.debug(*args, **kwargs)