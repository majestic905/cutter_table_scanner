import numpy as np
import json
import jsonschema
from scipy.interpolate import griddata
from server.src.app.logger import log_timing
from server.src.app.paths import CAMERAS_DATA_PATH, CAMERAS_SCHEMA_PATH, CAMERAS_MAPPINGS_PATH
from .position import CameraPosition


_mappings = None


def compute_mapping_matrix(points):
    destination = np.array([point['dst'] for point in points])
    source = np.array([point['src'] for point in points])

    bottom_right_x, bottom_right_y = source[-1]  # last points MUST be right lower corner of image
    img_height, img_width = bottom_right_x + 1, bottom_right_y + 1

    mgrid_x = slice(0, img_height - 1, complex(0, img_height))
    mgrid_y = slice(0, img_width - 1, complex(0, img_width))
    grid_x, grid_y = np.mgrid[mgrid_x, mgrid_y]
    grid_z = griddata(destination, source, (grid_x, grid_y), method='cubic')

    map_x = np.append([], [ar[:, 1] for ar in grid_z]).reshape(img_height, img_width).astype(np.float32)
    map_y = np.append([], [ar[:, 0] for ar in grid_z]).reshape(img_height, img_width).astype(np.float32)
    return np.array([map_x.transpose(), map_y.transpose()]).transpose()


def save_cameras_data(data: dict):
    with open(CAMERAS_DATA_PATH, 'w') as file:
        json.dump(data, file, indent=4)


def validate_cameras_data(data: dict):
    try:
        with open(CAMERAS_SCHEMA_PATH) as file:
            schema = json.load(file)

        jsonschema.validate(data, schema)
    except jsonschema.ValidationError as error:
        return str(error)

    for position in data:
        points = data[position]['interpolation_points']
        last_point_x, last_point_y = points[-1]['dst']
        max_x = max([point['dst'][0] for point in points])
        max_y = max([point['dst'][1] for point in points])

        if not (last_point_x == max_x and last_point_y == max_y):
            return f"{position}.interpolation_points: last point 'dst' must be bottom right corner"


def get_cameras_json():
    with open(CAMERAS_DATA_PATH) as file:
        return json.load(file)


@log_timing
def get_cameras_data():
    cameras = get_cameras_json()

    global _mappings
    if _mappings is None:
        print('Computing mappings start...')
        _mappings = {position: compute_mapping_matrix(cameras[position]['interpolation_points']) for position in cameras}
        print('Computing mappings finish!')

    for position in cameras:
        cameras[position]['mapping'] = _mappings[position]

    return {CameraPosition[position]: data for position, data in cameras.items()}
