import json
from datetime import datetime
from paths import SCAN_INFO_PATH


def read_scan_info():
    with open(SCAN_INFO_PATH) as file:
        return json.load(file)


def write_scan_info(scan_type: str):
    info = {
        'scan_type': scan_type,
        'created_at': int(datetime.now().timestamp() * 1000)
    }

    with open(SCAN_INFO_PATH, 'w') as file:
        json.dump(info, file, indent=4)


if not SCAN_INFO_PATH.exists():
    write_scan_info('unknown')