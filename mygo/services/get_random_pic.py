import requests
import random as rng
from fastapi.responses import JSONResponse
from static import all_file

url = 'https://drive.miyago9267.com/d/file/img/mygo/'

def get_random_pic(amount: int) -> list:
    """Return all mygo pictures"""
    try:
        files = all_file.file_list

        rng_pics = rng.sample(files, amount)

        pic_files = [{'url': url + item['file_name'], 'alt': item['name']} for item in rng_pics]

        return JSONResponse(status_code=200, content={'urls': pic_files})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400, content={'error': 'Fail to fetch images library.'})