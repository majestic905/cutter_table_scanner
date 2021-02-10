import repository
import cv2
import storage
import shutil
from datetime import datetime


class Scan:
    def __init__(self, scan_id: str = None):
        if scan_id is None:
            scan_id = str(datetime.now().timestamp())
            storage.create_scan_dir(scan_id)

        self.scan_id = scan_id

    @staticmethod
    def list():
        return storage.scans_list()

    def path_for(self, file: storage.ScanFile):
        if file == storage.ScanFile.PARAMS:
            return storage.path_for_params_file(self.scan_id)
        return storage.path_for_scan_image(self.scan_id, file)

    def persist_cv2_image(self, file: storage.ScanFile, cv2_image):
        path = storage.path_for_scan_image(self.scan_id, file)
        return cv2.imwrite(path, cv2_image)

    def persist_copy(self, file: storage.ScanFile, src_path):
        dst_path = storage.path_for_scan_image(self.scan_id, file)
        return shutil.copy(src_path, dst_path)

    def persist_capture(self, file: storage.ScanFile, camera):
        path = storage.path_for_scan_image(self.scan_id, file)
        return camera.capture_to_path(path)
