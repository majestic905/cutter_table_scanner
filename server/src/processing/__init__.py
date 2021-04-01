import numpy as np
import cv2
import exif
from pathlib import Path
from threading import Thread
from typing import Dict
from scipy.interpolate import griddata
from server.src.app.logger import log_timing
from server.src.camera import Camera, CameraPosition


ImagesType = Dict[CameraPosition, np.ndarray]
PathsType = Dict[CameraPosition, Path]
CamerasType = Dict[CameraPosition, Camera]


@log_timing
def _capture_photo(path: Path, camera: Camera):
    camera.capture_to_path(path)


def _disorient_image(path: Path):
    with open(path, 'rb') as file:
        image = exif.Image(file)
        image.orientation = '1'

    with open(path, 'wb') as file:
        file.write(image.get_file())


def _interpolate_table_section(image: np.ndarray, camera: Camera):
    # return cv2.remap(image, map_x, map_y, cv2.INTER_CUBIC)
    return cv2.remap(image, camera.mapping, None, cv2.INTER_CUBIC)


###############################################

@log_timing
def capture_photos(paths: PathsType, cameras: CamerasType):
    threads = {
        position: Thread(target=_capture_photo, args=(paths[position], cameras[position]))
        for position in CameraPosition
    }

    for position in CameraPosition:
        threads[position].start()

    for position in CameraPosition:
        threads[position].join()


@log_timing
def disorient_images(paths: PathsType):
    for position in CameraPosition:
        _disorient_image(paths[position])


@log_timing
def interpolate(images: ImagesType, cameras: CamerasType):
    return {position: _interpolate_table_section(images[position], cameras[position]) for position in cameras}


@log_timing
def compose(images: ImagesType):
    left_upper = images[CameraPosition.LU]
    right_upper = images[CameraPosition.RU]
    right_lower = images[CameraPosition.RL]
    left_lower = images[CameraPosition.LL]

    # horizontally
    upper = np.concatenate((left_upper, right_upper), axis=1)
    lower = np.concatenate((left_lower, right_lower), axis=1)

    # vertically
    return np.concatenate((upper, lower), axis=0)


def create_thumbnail(image: np.ndarray, width: int):
    if image is None:
        return None

    if width is None:
        raise ValueError('`width` is None')

    (h, w) = image.shape[:2]
    ratio = width / float(w)
    height = int(h * ratio)

    return cv2.resize(image, (width, height))
