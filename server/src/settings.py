import json
from jsonschema import validate, ValidationError
from camera import CameraPosition
from paths import SETTINGS_FILE_PATH, SETTINGS_SCHEMA_PATH


def _read_schema():
    with open(SETTINGS_SCHEMA_PATH) as file:
        return json.load(file)


def _read_settings():
    with open(SETTINGS_FILE_PATH) as file:
        return json.load(file)


def get_settings():
    return _settings


def save_settings(new_settings: dict):
    global _settings
    _settings = new_settings

    with open(SETTINGS_FILE_PATH, 'w') as file:
        json.dump(new_settings, file, indent=4)


def validate_settings(json: dict):
    try:
        validate(json, _schema)
    except ValidationError as error:
        if len(error.path) > 0:
            path = list(error.path)
            path = path[0] + "".join([f'[{str(item)}]' for item in path[1:]])
            return f'ERROR — {path}: {error.message}'
        else:
            return f'ERROR — {error.message}'

    sizes = {}
    for position in CameraPosition:
        [width, height] = json['cameras'][position.name]['projectied_image_size']
        sizes[position.name] = {'width': width, 'height': height}

    if sizes['LU']['width'] != sizes['LL']['width']:
        return f'ERROR — projectied_image_size: LU width and LL width must be equal'
    if sizes['LU']['height'] != sizes['RU']['height']:
        return f'ERROR — projectied_image_size: LU height and RU height must be equal'
    if sizes['RL']['width'] != sizes['RU']['width']:
        return f'ERROR — projectied_image_size: RL width and RU width must be equal'
    if sizes['RL']['height'] != sizes['LL']['height']:
        return f'ERROR — projectied_image_size: RL height and LL height must be equal'


_settings = _read_settings()
_schema = _read_schema()