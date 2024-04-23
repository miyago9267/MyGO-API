"""Router for Basic Info"""
import time
from fastapi import APIRouter
from services import get_pic, get_pic_list

router = APIRouter()

@router.get('/img')
async def get_mygo_pic(
    keyword: str
) -> dict:
    """Return a mygo picture with keyword"""
    return get_pic.get_pic(keyword)

@router.get('/all_img')
async def get_all_mygo_pic() -> dict:
    """Return all mygo pictures"""
    return get_pic_list.get_pic_list()