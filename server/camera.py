import os.path
import shutil
from enum import Enum


class CameraPosition(Enum):
    LU = 'left_upper'
    RU = 'right_upper'
    RL = 'right_lower'
    LL = 'left_lower'


class Camera:
    def __init__(self, position, address):
        self.position = position
        self.address = address

    def capture_to_path(self, path):
        dst_file_name = os.path.basename(path)
        dst_dir_path = os.path.dirname(path)

        src_file_path = os.path.join(dst_dir_path, '..', '..', 'eggs', 'sample_scan', dst_file_name)
        shutil.copy(src_file_path, path)

