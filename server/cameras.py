import os.path
import json
from camera import Camera
from server.constants.enums import CameraPosition
from server.constants.paths import CAMERAS_FILE_PATH


cameras_json = {
    position.name: {
        "maker": "",
        "model": "",
        "usb_port": "",
        "projection_points": {position.name: [0, 0] for position in CameraPosition}
    }
    for position in CameraPosition
}
cameras = {}


def read_cameras_json():
    global cameras_json
    with open(CAMERAS_FILE_PATH) as file:
        cameras_json = json.load(file)


def save_cameras_json():
    with open(CAMERAS_FILE_PATH, 'w') as file:
        json.dump(cameras_json, file)


def create_cameras():
    global cameras

    for position, data in cameras_json.items():
        position = CameraPosition[position]
        camera = Camera(data['usb_port'], data['maker'], data['model'], projection_points=data['projection_points'])
        cameras[position] = camera


def update_cameras_json(data: dict):
    global cameras_json, cameras
    cameras_json = data

    save_cameras_json()
    create_cameras()


if os.path.exists(CAMERAS_FILE_PATH):
    read_cameras_json()
    create_cameras()
else:
    save_cameras_json()
    create_cameras()