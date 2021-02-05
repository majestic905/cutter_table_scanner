import os.path
import shutil


class Camera:
    def __init__(self, some_id):
        self.some_id = some_id

    def capture_to(self, dst_file_path):
        dst_file_name = os.path.basename(dst_file_path)
        dst_dir_path = os.path.dirname(dst_file_path)

        src_file_path = os.path.join(dst_dir_path, '..', '..', 'venv', dst_file_name)
        shutil.copy(src_file_path, dst_file_path)
