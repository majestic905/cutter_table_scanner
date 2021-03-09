import numpy as np
import lensfunpy
import cv2
from cameras import Camera
from server.constants.enums import CameraPosition
from server.constants.custom_types import ImagesType


def undistort(image: np.ndarray, camera: Camera, exif: dict = None):
    # height, width = image.shape[0], image.shape[1]
    #
    # mod = lensfunpy.Modifier(camera.lf_lens, camera.lf_cam.crop_factor, width, height)
    #
    # focal_length = exif['focal_length']
    # aperture = exif['aperture']
    # distance = 2
    # mod.initialize(focal_length, aperture, distance)
    #
    # undist_coords = mod.apply_geometry_distortion()
    # return cv2.remap(image, undist_coords, None, cv2.INTER_LANCZOS4)

    return image


def project(image: np.ndarray, camera: Camera):
    pts = camera.projection_points
    lu, ru, rl, ll = pts[CameraPosition.LU], pts[CameraPosition.RU], pts[CameraPosition.RL], pts[CameraPosition.LL]

    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((rl['x'] - ll['x']) ** 2) + ((rl['y'] - ll['y']) ** 2))
    widthB = np.sqrt(((ru['x'] - lu['x']) ** 2) + ((ru['y'] - lu['y']) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((ru['x'] - rl['x']) ** 2) + ((ru['y'] - rl['y']) ** 2))
    heightB = np.sqrt(((lu['x'] - ll['x']) ** 2) + ((lu['y'] - ll['y']) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    src = np.array([
        [lu['x'], lu['y']],
        [ru['x'], ru['y']],
        [rl['x'], rl['y']],
        [ll['x'], ll['y']]], dtype="float32")

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(src, dst)
    return cv2.warpPerspective(image, M, (maxWidth, maxHeight))


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