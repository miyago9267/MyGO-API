"""
Danger!!! This module has READ FILE operation.
"""

import requests
from fastapi.responses import JSONResponse
from static import all_file

url = 'https://drive.miyago9267.com/d/file/img/mygo/'

def get_pic_list() -> list:
    """Return all mygo pictures"""
    try:
        files = all_file.file_list

        all_files = [{'url': url + item['file_name'], 'alt': item['name']} for item in files]

        return JSONResponse(status_code=200, content={'urls': all_files})
    except Exception as e:
        return JSONResponse(status_code=400, content={'error': 'Fail to fetch images library.'})