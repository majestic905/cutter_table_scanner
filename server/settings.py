import json
import shutil
import os

from server.constants.paths import SETTINGS_FILE_PATH


def _read_settings():
    with open(SETTINGS_FILE_PATH) as file:
        return json.load(file)


def save_settings(new_settings: dict):
    global _settings
    _settings = new_settings

    with open(SETTINGS_FILE_PATH, 'w') as file:
        json.dump(new_settings, file, indent=4)


def get_settings():
    return _settings


_settings = _read_settings()