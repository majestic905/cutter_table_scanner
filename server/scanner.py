import os.path
import shutil
import repository
from camera import Camera
from repository import File


cameras = {
    File.LEFT_UPPER: Camera('left_upper'),
    File.RIGHT_UPPER: Camera('right_upper'),
    File.RIGHT_LOWER: Camera('right_lower'),
    File.LEFT_LOWER: Camera('left_lower'),
}


def capture_to(file_paths):
    for file, camera in cameras.items():
        camera.capture_to(file_paths[file])


def process_images(file_paths):
    dst_file_path = file_paths[File.RESULT]

    dst_file_name = os.path.basename(dst_file_path)
    dst_dir_path = os.path.dirname(dst_file_path)

    src_file_path = os.path.join(dst_dir_path, '..', '..', 'venv', dst_file_name)
    shutil.copy(src_file_path, dst_file_path)


def perform_scan():
    file_paths = repository.create()
    capture_to(file_paths)
    process_images(file_paths)
