import numpy as np
from typing import Dict

from camera import Camera
from enums import CameraPosition

ImagesType = Dict[CameraPosition, np.ndarray]
CamerasType = Dict[CameraPosition, Camera]
PathsType = Dict[CameraPosition, str]