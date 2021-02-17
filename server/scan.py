import storage
from enums import ScanType, ScanFile

from datetime import datetime


class Scan:
    def __init__(self, type: ScanType):
        self.id = str(datetime.now().timestamp())
        self.type = scan_type

    def path_for(self, scan_file: ScanFile):
        return storage.path_for_scan_file(self.id, scan_file)
