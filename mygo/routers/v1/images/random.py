"""GET /api/v1/images/random - 獲取隨機圖片"""
from fastapi import Query, HTTPException
import random
from static import all_file

BASE_URL = 'https://drive.miyago9267.com/d/file/img/mygo/'

async def get_random_images(
    count: int = Query(1, ge=1, le=100, description="圖片數量（1-100）"),
    amount: int = Query(None, ge=1, le=100, description="圖片數量（別名，與 count 相同）")
):
    """
    獲取隨機圖片
    
    Query parameters:
    - count: 圖片數量（預設 1，最大 100）
    - amount: 圖片數量（別名，與 count 相同，用於向後相容）
    """
    try:
        files = all_file.file_list
        
        # 使用 amount 參數（如果提供）來覆蓋 count（向後相容）
        requested_count = amount if amount is not None else count
        
        if requested_count <= 0:
            raise HTTPException(status_code=400, detail="Count must be greater than 0")
        
        if requested_count > len(files):
            raise HTTPException(
                status_code=400,
                detail=f"Requested count ({requested_count}) exceeds available images ({len(files)})"
            )
        
        # 隨機選擇
        random_files = random.sample(files, requested_count)
        
        # 格式化回應
        random_images = [
            {
                'id': item.get('id'),
                'url': BASE_URL + item['file_name'],
                'alt': item['name'],
                'author': item.get('author'),
                'episode': item.get('episode')
            }
            for item in random_files
        ]
        
        return {
            'data': random_images,
            'meta': {
                'count': requested_count,
                'requested': requested_count
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Random images error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch random images")
