import os
import shutil
from server.app import app
from server.constants.enums import ScanFile, CameraPosition

DATA_DIR_PATH = os.path.join(app.static_folder, 'data')
SETTINGS_FILE_PATH = os.path.join(DATA_DIR_PATH, ScanFile.SETTINGS.value)
SCANS_DIR_PATH = os.path.join(DATA_DIR_PATH, 'scans')

# create server/static
if not os.path.exists(app.static_folder):
    os.mkdir(app.static_folder)

# create server/static/data
if not os.path.exists(DATA_DIR_PATH):
    os.mkdir(DATA_DIR_PATH)

# create server/static/data/scans
if not os.path.exists(SCANS_DIR_PATH):
    os.mkdir(SCANS_DIR_PATH)

# copy server/_settings.json to server/static/data/settings.json
if not os.path.exists(SETTINGS_FILE_PATH):
    src = os.path.join(app.root_path, '_settings.json')
    shutil.copy(src, SETTINGS_FILE_PATH)

# copy server/_cameras.xml to ~/AppData/Local/lensfun/cameras.xml or ~/.local/share/lensfun/cameras.xml
if os.name == "nt":
    lf_folder = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'lensfun')
else:
    lf_folder = os.path.join(os.path.expanduser('~'), '.local', 'share', 'lensfun')

if not os.path.exists(lf_folder):
    os.mkdir(lf_folder)

cameras_file = os.path.join(lf_folder, 'cameras.xml')

if not os.path.exists(cameras_file):
    src = os.path.join(app.root_path, '_cameras.xml')
    shutil.copy(src, cameras_file)
