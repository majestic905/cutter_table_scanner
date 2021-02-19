import numpy as np
from typing import Dict

from server.camera import Camera
from server.constants.enums import CameraPosition

ImagesType = Dict[CameraPosition, np.ndarray]
CamerasType = Dict[CameraPosition, Camera]
PathsType = Dict[CameraPosition, str]