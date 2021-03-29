import numpy as np
import cv2
import exif
from pathlib import Path
from threading import Thread
from multiprocessing import Process
from typing import Dict
from server.src.app.logger import log_timing
from server.src.camera import Camera, CameraPosition
from .lensfun import get_undist_coords


ImagesType = Dict[CameraPosition, np.ndarray]
PathsType = Dict[CameraPosition, Path]
CamerasType = Dict[CameraPosition, Camera]


def _capture_photo(path: Path, camera: Camera):
    camera.capture_to_path(path)


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


def _disorient_image(path: Path):
    with open(path, 'rb') as file:
        image = exif.Image(file)
        image.orientation = '1'

    with open(path, 'wb') as file:
        file.write(image.get_file())


@log_timing
def disorient_images(paths: PathsType):
    for position in CameraPosition:
        _disorient_image(paths[position])


@log_timing
def _undistort_image(path: Path, image: np.ndarray, camera: Camera):
    if not camera.lf_cam or not camera.lf_lens:
        return image

    height, width = image.shape[0], image.shape[1]
    undist_coords = get_undist_coords(camera, (width, height))
    result = cv2.remap(image, undist_coords, None, cv2.INTER_LANCZOS4)
    cv2.imwrite(str(path), result)


@log_timing
def undistort(paths: PathsType, images: ImagesType, cameras: CamerasType):
    processes = {
        position: Process(target=_undistort_image, args=(paths[position], images[position], cameras[position]))
        for position in CameraPosition
    }

    for position in CameraPosition:
        processes[position].start()

    for position in CameraPosition:
        processes[position].join()


def _draw_polygon(image: np.ndarray, camera: Camera):
    points = camera.projection_points
    points = [points['top_left'], points['top_right'], points['bottom_right'], points['bottom_left']]
    points = np.array(points, dtype=np.int32).reshape((-1, 1, 2))
    return cv2.polylines(image, [points], True, (0, 0, 255), thickness=8)


@log_timing
def draw_polygons(images, cameras):
    return {position: _draw_polygon(images[position], cameras[position]) for position in cameras}


def _project_image(image: np.ndarray, camera: Camera):
    points = camera.projection_points
    dst_width, dst_height = camera.projected_image_size
    img_height, img_width = image.shape[:2]

    for pt_x, pt_y in points.values():
        if not 0 <= pt_x < img_width or not 0 <= pt_y < img_height:
            raise IndexError('One of projection_points falls outside of image')

    src_points = [points['top_left'], points['top_right'], points['bottom_right'], points['bottom_left']]
    src_points = np.array(src_points, dtype=np.float32)
    dst_points = np.array([[0, 0], [dst_width - 1, 0], [dst_width - 1, dst_height - 1], [0, dst_height - 1]], dtype=np.float32)

    M = cv2.getPerspectiveTransform(src_points, dst_points)
    return cv2.warpPerspective(image, M, (dst_width, dst_height))


@log_timing
def project(images: ImagesType, cameras: CamerasType):
    return {position: _project_image(images[position], cameras[position]) for position in cameras}


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
