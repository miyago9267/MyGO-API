"""GET /api/v1/images/{id} - 獲取特定圖片詳情"""
from fastapi import HTTPException, Path as PathParam
from static import all_file

BASE_URL = 'https://drive.miyago9267.com/d/file/img/mygo/'

async def get_image_detail(
    image_id: int = PathParam(..., description="圖片 ID")
):
    """
    獲取特定圖片詳情
    
    Path parameters:
    - image_id: 圖片的唯一識別碼
    """
    try:
        files = all_file.file_list
        
        # 查找圖片
        image_item = None
        for item in files:
            if item.get('id') == image_id:
                image_item = item
                break
        
        if not image_item:
            raise HTTPException(status_code=404, detail="Image not found")
        
        return {
            'data': {
                'id': image_item.get('id'),
                'url': BASE_URL + image_item['file_name'],
                'alt': image_item['name'],
                'author': image_item.get('author'),
                'episode': image_item.get('episode'),
                'filename': image_item['file_name']
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Get image detail error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch image details")
