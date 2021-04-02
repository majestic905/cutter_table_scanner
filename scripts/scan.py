import json
import numpy as np
import cv2
from scipy.interpolate import griddata
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple


POSITIONS = ['LL', 'RL', 'RU', 'LU']
IMAGES_DIR = Path('.') / 'images'
CAMERAS_JSON = IMAGES_DIR / 'cameras.json'


def read_images():
    paths = {position: str(IMAGES_DIR / f'{position}_original.jpg') for position in POSITIONS}
    return {position: cv2.imread(path) for position, path in paths.items()}


def read_json():
    with open(CAMERAS_JSON) as file:
        return json.load(file)


def compute_mapping(points):
    destination = np.array([point['dst'] for point in points])
    source = np.array([point['src'] for point in points])

    bottom_right_x, bottom_right_y = destination[-1]  # last points MUST be right lower corner of image
    img_height, img_width = bottom_right_x + 1, bottom_right_y + 1

    mgrid_x = slice(0, img_height - 1, complex(0, img_height))
    mgrid_y = slice(0, img_width - 1, complex(0, img_width))
    grid_x, grid_y = np.mgrid[mgrid_x, mgrid_y]
    grid_z = griddata(destination, source, (grid_x, grid_y), method='cubic')

    map_x = np.append([], [ar[:, 1] for ar in grid_z]).reshape(img_height, img_width).astype(np.float32)
    map_y = np.append([], [ar[:, 0] for ar in grid_z]).reshape(img_height, img_width).astype(np.float32)
    return map_x, map_y


def interpolate_image(image, points, position):
    print(f'Working on image {position}')
    map_x, map_y = compute_mapping(points)
    return cv2.remap(image, map_x, map_y, cv2.INTER_CUBIC)


def interpolate(images, points):
    return {position: interpolate_image(images[position], points[position], position) for position in images}


def compose(images):
    upper = np.concatenate((images['LU'], images['RU']), axis=1)
    lower = np.concatenate((images['LL'], images['RL']), axis=1)
    return np.concatenate((upper, lower), axis=0)


if __name__ == '__main__':
    start = datetime.now()

    images = read_images()
    cameras = read_json()
    points = {position: cameras[position]['interpolation_points'] for position in cameras}
    images = interpolate(images, points)
    result = compose(images)

    result_path = str(IMAGES_DIR / 'result.jpg')
    cv2.imwrite(result_path, result)

    end = datetime.now()
    print(f'Took {round(end - start, 2)} seconds')