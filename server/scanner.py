import os.path
import shutil
from scan import Scan
from camera import Camera, CameraPosition
from storage import ScanFile


cameras = {
    CameraPosition.LU: Camera(CameraPosition.LU.value),
    CameraPosition.RU: Camera(CameraPosition.RU.value),
    CameraPosition.RL: Camera(CameraPosition.RL.value),
    CameraPosition.LL: Camera(CameraPosition.LL.value),
}


def process_images(file_paths):
    dst_file_path = file_paths[ScanFile.RESULT]

    dst_file_name = os.path.basename(dst_file_path)
    dst_dir_path = os.path.dirname(dst_file_path)

    src_file_path = os.path.join(dst_dir_path, '..', '..', 'eggs', 'sample_scan', dst_file_name)
    shutil.copy(src_file_path, dst_file_path)


def perform_scan():
    scan = Scan()

    for camera_position, camera in cameras.items():
        scan.capture_original(camera, camera_position)

    process_images()