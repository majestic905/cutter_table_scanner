import json
import jsonschema
from server.src.app.paths import CAMERAS_DATA_PATH, CAMERAS_SCHEMA_PATH
from .position import CameraPosition


def _read_data():
    with open(CAMERAS_DATA_PATH) as file:
        cameras = json.load(file)
        return {CameraPosition[position]: data for position, data in cameras.items()}


def _read_schema():
    with open(CAMERAS_SCHEMA_PATH) as file:
        return json.load(file)


def save_cameras_data(data: dict):
    with open(CAMERAS_DATA_PATH, 'w') as file:
        json.dump(data, file, indent=4)

    global _data
    _data = _read_data()


def validate_cameras_data(data: dict):
    try:
        jsonschema.validate(data, _schema)
    except jsonschema.ValidationError as error:
        return str(error)

    sizes = {}
    for position in data:
        width, height = data[position]['projected_image_size']
        sizes[position] = {'width': width, 'height': height}

    if sizes['LU']['width'] != sizes['LL']['width']:
        return f'projected_image_size: LU width and LL width must be equal'
    if sizes['LU']['height'] != sizes['RU']['height']:
        return f'projected_image_size: LU height and RU height must be equal'
    if sizes['RL']['width'] != sizes['RU']['width']:
        return f'projected_image_size: RL width and RU width must be equal'
    if sizes['RL']['height'] != sizes['LL']['height']:
        return f'projected_image_size: RL height and LL height must be equal'


def get_cameras_data():
    return _data


_data = _read_data()
_schema = _read_schema()