import numpy as np
import lensfunpy
import cv2
from typing import Dict
from camera_position import CameraPosition
from cameras import Camera

ImagesType = Dict[CameraPosition, np.ndarray]
CamerasType = Dict[CameraPosition, Camera]
PathsType = Dict[CameraPosition, str]


def _undistort_image(image: np.ndarray, camera: Camera):
    height, width = image.shape[0], image.shape[1]

    mod = lensfunpy.Modifier(camera.lf_lens, camera.lf_cam.crop_factor, width, height)
    mod.initialize(camera.lf_lens.min_focal, 0, 0)  # aperture and focus distance are not used for distortion

    undist_coords = mod.apply_geometry_distortion()
    return cv2.remap(image, undist_coords, None, cv2.INTER_LANCZOS4)


def _draw_polygon(image: np.ndarray, camera: Camera):
    points = camera.projection_points
    points = np.array([points[key] for key in ['top_left', 'top_right', 'bottom_right', 'bottom_left']], dtype=np.int32)
    points = points.reshape((-1, 1, 2))
    return cv2.polylines(image, [points], True, (0,0,255), thickness=8)


def _project_image(image: np.ndarray, camera: Camera):
    points = camera.projection_points
    width, height = camera.projection_image_size

    keys = ['top_left', 'top_right', 'bottom_right', 'bottom_left']
    for key in keys:
        pt_x, pt_y = points[key]
        if not 0 < pt_x < width or 0 < pt_y < height:
            raise IndexError('One of projection_points falls outside of image')

    src = np.array([points[key] for key in keys], dtype=np.float32)
    dst = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(src, dst)
    return cv2.warpPerspective(image, M, (width, height))


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


def read_images(paths: PathsType):
    return {position: cv2.imread(paths[position]) for position in paths}


def persist_image(path, image):
    cv2.imwrite(path, image)


def persist_images(paths: PathsType, images: ImagesType):
    for key in images:
        persist_image(paths[key], images[key])


def capture_photos(paths: PathsType, cameras: CamerasType):
    for position, camera in cameras.items():
        # scan.log(f'Capture START, {position.value}, {repr(camera)}')
        camera.capture_to_path(paths[position])
        # scan.log(f'Capture END, {position.value}, {repr(camera)}')

def undistort(images: ImagesType, cameras: CamerasType):
    # scan.log('Building undistorted images...')
    return {position: _undistort_image(images[position], cameras[position]) for position in cameras}


def draw_polygons(images, cameras):
    # scan.log('Drawing polygons on undistorted images...')
    return {position: _draw_polygon(images[position], cameras[position]) for position in cameras}


def project(images: ImagesType, cameras: CamerasType):
    # scan.log('Building projected images...')
    return {position: _project_image(images[position], cameras[position]) for position in cameras}