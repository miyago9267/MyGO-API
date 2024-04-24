"""
Danger!!! This module has READ FILE operation.
"""

import requests
from fastapi.responses import JSONResponse

url = 'https://drive.miyago9267.com/d/home/miyago/Pictures/mygo/'

def get_pic_list() -> list:
    """Return all mygo pictures"""
    try:
        files = requests.get('http://127.0.0.1:9014/pic_list').json()

        all_files = [url + item for item in files]

        return JSONResponse(status_code=200, content={'urls': all_files})
    except Exception as e:
        return JSONResponse(status_code=400, content={'error': 'Fail to fetch images library.'})