"""Router for Basic Info"""
import time
from fastapi import APIRouter
from services import get_pic_multikey, get_pic_list, get_random_pic

router = APIRouter()

@router.get('/img')
async def get_mygo_pic(
    keyword: str,
    fuzzy: bool = True
) -> dict:
    """Return a mygo picture with keyword"""
    keywords = keyword.split(' ')
    return get_pic_multikey.get_pic(keywords, fuzzy)

@router.get('/all_img')
async def get_all_mygo_pic() -> dict:
    """Return all mygo pictures"""
    return get_pic_list.get_pic_list()

@router.get('/random_img')
async def get_random_mygo_pic(
    amount: int = 20
) -> dict:
    """Return random mygo pictures in amount"""
    return get_random_pic.get_random_pic(amount)