"""Images API Router"""
from fastapi import APIRouter
from . import index, search, random, detail

router = APIRouter()

# GET /api/v1/images - 獲取所有圖片列表（支援分頁）
router.add_api_route(
    "",
    index.get_images,
    methods=["GET"],
    summary="獲取圖片列表",
    description="獲取所有圖片列表，支援分頁和排序"
)

# GET /api/v1/images/search - 搜尋圖片
router.add_api_route(
    "/search",
    search.search_images,
    methods=["GET"],
    summary="搜尋圖片",
    description="根據關鍵字搜尋圖片，支援模糊搜尋"
)

# GET /api/v1/images/random - 獲取隨機圖片
router.add_api_route(
    "/random",
    random.get_random_images,
    methods=["GET"],
    summary="獲取隨機圖片",
    description="獲取指定數量的隨機圖片"
)

# GET /api/v1/images/{id} - 獲取特定圖片詳情
router.add_api_route(
    "/{image_id}",
    detail.get_image_detail,
    methods=["GET"],
    summary="獲取圖片詳情",
    description="根據 ID 獲取特定圖片的詳細資訊"
)
