"""GET /api/v1/images/search - 搜尋圖片"""
from typing import Optional
from fastapi import Query, HTTPException
from static import all_file
from algo.Levenshtein import distance as levenshtein_distance
from opencc import OpenCC
import json
from pathlib import Path

BASE_URL = 'https://drive.miyago9267.com/d/file/img/mygo/'
cc = OpenCC('s2t')

# 載入自定義關鍵字映射
json_path = Path(__file__).parent.parent.parent.parent / 'static' / 'mygo.json'
with json_path.open('r', encoding='utf-8') as f:
    custom_keymap = json.load(f)

fuzzy_replacements = {
    "你": ["妳"],
    "妳": ["你"],
    "他": ["她"],
    "她": ["他"],
    "欸": ["耶"],
    "耶": ["欸"],
}

def generate_fuzzy_variants(keyword):
    """產生模糊搜尋變體"""
    variants = {keyword}
    for i, char in enumerate(keyword):
        if char in fuzzy_replacements:
            for replacement in fuzzy_replacements[char]:
                new_variant = keyword[:i] + replacement + keyword[i+1:]
                variants.add(new_variant)
    return variants

async def search_images(
    q: str = Query(..., description="搜尋關鍵字"),
    fuzzy: bool = Query(False, description="是否啟用模糊搜尋"),
    page: int = Query(1, ge=1, description="頁碼（從 1 開始）"),
    limit: int = Query(20, ge=1, le=100, description="每頁數量（1-100）"),
    order: str = Query("id", description="排序方式")
):
    """
    搜尋圖片，支援模糊搜尋和繁簡互搜
    
    Query parameters:
    - q: 搜尋關鍵字
    - fuzzy: 是否啟用模糊搜尋（預設 false）
    - page: 頁碼（預設 1）
    - limit: 每頁數量（預設 20）
    - order: 排序方式（預設 id）
    """
    try:
        # 驗證搜尋關鍵字
        if not q or not q.strip():
            raise HTTPException(status_code=400, detail="Search query is required")
        
        # 轉換繁體中文
        keywords = [cc.convert(keyword.strip()) for keyword in q.split()]
        
        files = all_file.file_list
        scored_results = []
        
        # 搜尋邏輯
        for item in files:
            name = item['name']
            total_score = 0
            
            # 檢查自定義關鍵字映射
            custom_match = False
            for keyword in keywords:
                if keyword in custom_keymap:
                    if name in custom_keymap[keyword].get('value', []):
                        total_score = 15
                        custom_match = True
                        break
            
            if not custom_match:
                # 原有搜尋算法
                for keyword in keywords:
                    fuzzy_variants = generate_fuzzy_variants(keyword) if fuzzy else {keyword}
                    max_score_for_keyword = 0
                    
                    for variant in fuzzy_variants:
                        if variant == name:
                            max_score_for_keyword = max(max_score_for_keyword, 15)
                        elif variant in name:
                            max_score_for_keyword = max(max_score_for_keyword, 10)
                        elif fuzzy and len(variant) > 2 and len(name) > 2:
                            distance = levenshtein_distance(variant, name)
                            if distance <= 2:
                                similarity_ratio = (len(variant) - distance) / len(variant)
                                if similarity_ratio >= 0.5:
                                    max_score_for_keyword = max(max_score_for_keyword, 3)
                    
                    if max_score_for_keyword > 0:
                        total_score += max_score_for_keyword
                    else:
                        # 關鍵字未匹配，跳過此項目
                        total_score = 0
                        break
            
            if total_score > 0:
                scored_results.append({
                    'id': item.get('id'),
                    'url': BASE_URL + item['file_name'],
                    'alt': item['name'],
                    'author': item.get('author'),
                    'episode': item.get('episode'),
                    'score': total_score
                })
        
        # 排序結果（按分數降序）
        sorted_results = sorted(scored_results, key=lambda x: x['score'], reverse=True)
        
        # 移除 score 欄位（內部使用）
        for result in sorted_results:
            result.pop('score', None)
        
        # 分頁
        total = len(sorted_results)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        
        if start_idx >= total and total > 0:
            raise HTTPException(status_code=404, detail="Page not found")
        
        paginated_results = sorted_results[start_idx:end_idx]
        
        return {
            'data': paginated_results,
            'meta': {
                'page': page,
                'limit': limit,
                'total': total,
                'totalPages': (total + limit - 1) // limit if total > 0 else 0,
                'hasNext': end_idx < total,
                'hasPrev': page > 1,
                'query': q,
                'fuzzy': fuzzy
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Search error: {e}")
        raise HTTPException(status_code=500, detail="Failed to search images")
