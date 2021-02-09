import os.path
import shutil
import repository
from camera import Camera
from repository import File
from improc import process_images


cameras = {
    File.LEFT_UPPER: Camera('left_upper'),
    File.RIGHT_UPPER: Camera('right_upper'),
    File.RIGHT_LOWER: Camera('right_lower'),
    File.LEFT_LOWER: Camera('left_lower'),
}


def capture_photos(file_paths):
    for file, camera in cameras.items():
        camera.capture_to(file_paths[file])


def perform_scan():
    file_paths = repository.create_item()
    capture_photos(file_paths)
    process_images(file_paths)
