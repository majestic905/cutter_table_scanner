import numpy as np
import lensfunpy
import cv2
from cameras import Camera, CameraPosition
from server.constants.custom_types import ImagesType


def undistort(image: np.ndarray, camera: Camera):
    height, width = image.shape[0], image.shape[1]

    mod = lensfunpy.Modifier(camera.lf_lens, camera.lf_cam.crop_factor, width, height)
    mod.initialize(camera.lf_lens.min_focal, 0, 0)  # aperture and focus distance

    undist_coords = mod.apply_geometry_distortion()
    return cv2.remap(image, undist_coords, None, cv2.INTER_LANCZOS4)


def project(image: np.ndarray, camera: Camera):
    points = camera.projection_points
    width, height = camera.projection_image_size

    src = np.array([points[key] for key in ['top_left', 'top_right', 'bottom_right', 'bottom_left']], dtype='float32')
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