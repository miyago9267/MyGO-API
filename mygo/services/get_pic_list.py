"""
Danger!!! This module has READ FILE operation.
"""

import requests
from fastapi.responses import JSONResponse

def get_pic_list() -> list:
    """Return all mygo pictures"""
    all_files = requests.get('http://127.0.0.1:9014/pic_list')

    return JSONResponse(content=all_files.json())