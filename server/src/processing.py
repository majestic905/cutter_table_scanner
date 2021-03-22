import numpy as np
import lensfunpy
import cv2
from typing import Dict
from camera import Camera, CameraPosition, CamerasType


_PROJECTION_POINTS_KEYS = ['top_left', 'top_right', 'bottom_right', 'bottom_left']


ImagesType = Dict[CameraPosition, np.ndarray]
PathsType = Dict[CameraPosition, str]


def _undistort_image(image: np.ndarray, camera: Camera):
    height, width = image.shape[0], image.shape[1]

    mod = lensfunpy.Modifier(camera.lf_lens, camera.lf_cam.crop_factor, width, height)
    mod.initialize(camera.lf_lens.min_focal, 0, 0)  # aperture and focus distance are not used for distortion

    undist_coords = mod.apply_geometry_distortion()
    return cv2.remap(image, undist_coords, None, cv2.INTER_LANCZOS4)


def _draw_polygon(image: np.ndarray, camera: Camera):
    points = camera.projection_points
    points = np.array([points[key] for key in _PROJECTION_POINTS_KEYS], dtype=np.int32)
    points = points.reshape((-1, 1, 2))
    return cv2.polylines(image, [points], True, (0,0,255), thickness=8)


def _project_image(image: np.ndarray, camera: Camera):
    points = camera.projection_points
    dst_width, dst_height = camera.projection_image_size
    img_height, img_width = image.shape[:2]

    for pt_x, pt_y in points.values():
        if not 0 <= pt_x < img_width or not 0 <= pt_y < img_height:
            raise IndexError('One of projection_points falls outside of image')

    src_points = np.array([points[key] for key in _PROJECTION_POINTS_KEYS], dtype=np.float32)
    dst_points = np.array([[0, 0], [dst_width - 1, 0], [dst_width - 1, dst_height - 1], [0, dst_height - 1]], dtype=np.float32)

    M = cv2.getPerspectiveTransform(src_points, dst_points)
    return cv2.warpPerspective(image, M, (dst_width, dst_height))


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


def undistort(images: ImagesType, cameras: CamerasType):
    return {position: _undistort_image(images[position], cameras[position]) for position in cameras}


def draw_polygons(images, cameras):
    return {position: _draw_polygon(images[position], cameras[position]) for position in cameras}


def project(images: ImagesType, cameras: CamerasType):
    return {position: _project_image(images[position], cameras[position]) for position in cameras}


def create_thumbnail(image: np.ndarray, width: int):
    if image is None:
        return None

    if width is None:
        raise ValueError('`width` is None')

    (h, w) = image.shape[:2]
    ratio = width / float(w)
    height = int(h * ratio)

    return cv2.resize(image, (width, height))
