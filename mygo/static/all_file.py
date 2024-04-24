import requests

file_list = requests.get('http://127.0.0.1:9014/pic_list').json()