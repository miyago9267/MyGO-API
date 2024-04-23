from static import all_file
from pathlib import Path
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

json_path = Path(__file__).parent.parent / 'static' / 'mygo.json'

with json_path.open('r', encoding='utf-8') as f:
    data = json.load(f)

url = 'https://drive.miyago9267.com/d/home/miyago/Pictures/mygo/'
all_pics = all_file.file_list

def get_pic(keyword: str):
    if keyword in data.keys():
        urls = data.get(keyword, {}).get('value', [])
        updated_urls = [url + item for item in urls]
        return JSONResponse(status_code=200, content={'urls': updated_urls})

    for item in all_pics:
        if keyword in item:
            return JSONResponse(status_code=200, content={'url': [url + item]})

    else:
        return HTTPException(status_code=404, detail='Not Found')