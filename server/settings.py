import json
from jsonschema import validate, ValidationError
from server.constants.paths import SETTINGS_FILE_PATH, SETTINGS_SCHEMA_PATH


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
        path = list(error.path)
        path = path[0] + "".join([f'[{str(item)}]' for item in path[1:]])
        return f'ERROR — {path}: {error.message}'


_settings = _read_settings()
_schema = _read_schema()