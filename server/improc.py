import os.path
import shutil
from repository import File


def undistort(image):
    return image


def project(image):
    return image


def process_images(file_paths):
    dst_file_path = file_paths[File.RESULT]

    dst_file_name = os.path.basename(dst_file_path)
    dst_dir_path = os.path.dirname(dst_file_path)

    src_file_path = os.path.join(dst_dir_path, '..', '..', 'eggs', 'sample_scan', dst_file_name)
    shutil.copy(src_file_path, dst_file_path)
