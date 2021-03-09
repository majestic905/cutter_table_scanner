import numpy as np
from typing import Dict

from server.cameras import Camera
from server.constants.enums import CameraPosition

ImagesType = Dict[CameraPosition, np.ndarray]
CamerasType = Dict[CameraPosition, Camera]
ExifType = Dict[CameraPosition, Dict[str, float]]
PathsType = Dict[CameraPosition, str]