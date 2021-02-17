import os
import shutil
from datetime import datetime
from enums import CameraPosition, ScanFile, ImageLevel, ScanType


DATA_DIR_PATH = os.path.join(os.path.dirname(__file__), 'data')
PARAMS_FILE_PATH = os.path.join(os.path.dirname(__file__), 'data', ScanFile.PARAMS.value)
SCANS_DIR_PATH = os.path.join(os.path.dirname(__file__), 'data', 'scans')