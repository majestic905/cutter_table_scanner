import numpy as np
import lensfunpy
import cv2
from camera import Camera
from server.constants.enums import CameraPosition
from server.constants.custom_types import ImagesType


def undistort(image: np.ndarray, camera: Camera):
    height, width = image.shape[0], image.shape[1]

    mod = lensfunpy.Modifier(camera.lf_lens, camera.lf_cam.crop_factor, width, height)
    # TODO: read exif
    # mod.initialize(focal_length, aperture, distance)

    undist_coords = mod.apply_geometry_distortion()
    return cv2.remap(image, undist_coords, None, cv2.INTER_LANCZOS4)


def project(image: np.ndarray, camera: Camera):
    return image


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