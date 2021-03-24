import numpy as np
import lensfunpy
import cv2
import exif
from app_logger import logger
from pathlib import Path
from threading import Thread
from typing import Dict
from timeit import default_timer as timer
from camera import Camera, CameraPosition


ImagesType = Dict[CameraPosition, np.ndarray]
PathsType = Dict[CameraPosition, Path]
CamerasType = Dict[CameraPosition, Camera]


def _capture_photo(path: Path, camera: Camera):
    camera.capture_to_path(path)


def capture_photos(paths: PathsType, cameras: CamerasType):
    threads = {
        position: Thread(target=_capture_photo, args=(paths[position], cameras[position]))
        for position in CameraPosition
    }

    start = timer()
    logger.debug('[capture_photos] start')

    for position in CameraPosition:
        threads[position].start()

    for position in CameraPosition:
        threads[position].join()

    end = timer()
    logger.debug(f'[capture_photos] end, took {round(end - start, 2)} seconds')


def _disorient_image(path: Path):
    with open(path, 'rb') as file:
        image = exif.Image(file)
        image.orientation = '1'

    with open(path, 'wb') as file:
        file.write(image.get_file())


def disorient_images(paths: PathsType):
    for position in CameraPosition:
        _disorient_image(paths[position])


def _flip_image(image: np.ndarray):  # flipCode: 0 - vertically, 1 - horizontally, -1 - both
    return cv2.flip(image, -1)


def flip_images(images: ImagesType):
    return {position: _flip_image(images[position]) for position in CameraPosition}


def _undistort_image(image: np.ndarray, camera: Camera):
    if not camera.lf_cam or not camera.lf_lens:
        return image

    height, width = image.shape[0], image.shape[1]

    mod = lensfunpy.Modifier(camera.lf_lens, camera.lf_cam.crop_factor, width, height)
    mod.initialize(camera.lf_lens.min_focal, 0, 0)  # aperture and focus distance are not used for distortion

    undist_coords = mod.apply_geometry_distortion()
    return cv2.remap(image, undist_coords, None, cv2.INTER_LANCZOS4)


def undistort(images: ImagesType, cameras: CamerasType):
    return {position: _undistort_image(images[position], cameras[position]) for position in cameras}


def _draw_polygon(image: np.ndarray, camera: Camera):
    points = camera.projection_points
    points = [points['top_left'], points['top_right'], points['bottom_right'], points['bottom_left']]
    points = np.array(points, dtype=np.int32).reshape((-1, 1, 2))
    return cv2.polylines(image, [points], True, (0,0,255), thickness=8)


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


def project(images: ImagesType, cameras: CamerasType):
    return {position: _project_image(images[position], cameras[position]) for position in cameras}


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
