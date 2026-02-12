"""GET /api/v1/images - 獲取圖片列表"""
from typing import Optional
from fastapi import Query, HTTPException
from static import all_file

BASE_URL = 'https://drive.miyago9267.com/d/file/img/mygo/'

async def get_images(
    page: int = Query(1, ge=1, description="頁碼（從 1 開始）"),
    limit: int = Query(20, ge=1, le=100, description="每頁數量（1-100）"),
    order: str = Query("id", description="排序方式: id, random, episode, alphabetical, popularity")
):
    """
    獲取所有圖片列表，支援分頁
    
    針對無限滾動優化的 API
    
    Query parameters:
    - page: 頁碼（預設 1，從 1 開始）
    - limit: 每頁數量（預設 20，建議 10-50 之間）
    - order: 排序方式（預設按 ID 升序）
        - id: 按 ID 數字順序排序
        - random: 隨機排序
        - episode: 按集數排序
        - alphabetical: 按字典序排序
        - popularity: 按人氣排序
    """
    try:
        files = all_file.file_list
        
        # 排序邏輯
        if order == "random":
            import random
            sorted_files = random.sample(files, len(files))
        elif order == "alphabetical":
            sorted_files = sorted(files, key=lambda x: x['name'])
        elif order == "episode":
            # 按照 episode 排序，mygo_x 優先於 mujica_x
            def episode_key(item):
                name = item.get('name', '')
                if 'mygo_' in name:
                    try:
                        ep_num = int(name.split('mygo_')[1].split('_')[0])
                        return (0, ep_num)
                    except:
                        return (2, 0)
                elif 'mujica_' in name:
                    try:
                        ep_num = int(name.split('mujica_')[1].split('_')[0])
                        return (1, ep_num)
                    except:
                        return (2, 0)
                return (2, 0)
            sorted_files = sorted(files, key=episode_key)
        else:  # id 或其他預設
            sorted_files = sorted(files, key=lambda x: x.get('id', 0))
        
        # 分頁邏輯
        total = len(sorted_files)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        
        if start_idx >= total and total > 0:
            raise HTTPException(status_code=404, detail="Page not found")
        
        paginated_files = sorted_files[start_idx:end_idx]
        
        # 格式化回應
        images = [
            {
                'id': item.get('id'),
                'url': BASE_URL + item['file_name'],
                'alt': item['name'],
                'author': item.get('author'),
                'episode': item.get('episode')
            }
            for item in paginated_files
        ]
        
        return {
            'data': images,
            'meta': {
                'page': page,
                'limit': limit,
                'total': total,
                'totalPages': (total + limit - 1) // limit,
                'hasNext': end_idx < total,
                'hasPrev': page > 1
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch images library")
