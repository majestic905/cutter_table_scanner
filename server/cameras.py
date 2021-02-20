import os.path
import json
from camera import Camera
from server.constants.enums import CameraPosition
from server.constants.paths import CAMERAS_FILE_PATH


cameras = {}


def read_cameras_data():
    with open(CAMERAS_FILE_PATH) as file:
        return json.load(file)


def save_cameras_data(data: dict):
    with open(CAMERAS_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)


def create_cameras(data: dict):
    global cameras
    for position, data in data.items():
        position = CameraPosition[position]
        camera = Camera(data['usb_port'], data['maker'], data['model'], projection_points=data['projection_points'])
        cameras[position] = camera


def update_cameras_data(data: dict):
    save_cameras_data(data)
    create_cameras(data)


if os.path.exists(CAMERAS_FILE_PATH):
    data = read_cameras_data()
    create_cameras(data)
else:
    projection_points = {position.name: [0, 0] for position in CameraPosition}
    data = {
        position.name: {"maker": "", "model": "", "usb_port": "", "projection_points": projection_points}
        for position in CameraPosition
    }
    save_cameras_data(data)
    create_cameras(data)