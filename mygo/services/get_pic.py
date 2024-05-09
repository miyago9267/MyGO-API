from static import all_file
from pathlib import Path
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

json_path = Path(__file__).parent.parent / 'static' / 'mygo.json'

with json_path.open('r', encoding='utf-8') as f:
    data = json.load(f)

url = 'https://drive.miyago9267.com/d/file/img/mygo/'
all_pics = all_file.file_list

def get_pic(keyword: str, fuzzy: bool = True):
    urls = []
    if fuzzy:
        urls += [{'url':url + item, 'alt':item[:-4]} for item in all_pics if keyword in item]
    if keyword in data.keys():
        urls += [{'url':url + item + '.png', 'alt':item} for item in data.get(keyword, {}).get('value', [])]
    unique_items = set(tuple(sorted(d.items())) for d in urls)

    urls = [dict(items) for items in unique_items]
    if not urls:
        return JSONResponse(status_code=200, content={'urls': []})
    else:
        return JSONResponse(status_code=200, content={'urls': urls})