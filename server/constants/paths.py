import os.path
import json
from server.app import app
from server.constants.enums import ScanFile, CameraPosition

DATA_DIR_PATH = os.path.join(app.static_folder, 'data')
CAMERAS_FILE_PATH = os.path.join(DATA_DIR_PATH, ScanFile.CAMERAS.value)
SCANS_DIR_PATH = os.path.join(DATA_DIR_PATH, 'scans')


if not os.path.exists(DATA_DIR_PATH):
    os.mkdir(DATA_DIR_PATH)

if not os.path.exists(SCANS_DIR_PATH):
    os.mkdir(SCANS_DIR_PATH)