from static import all_file
from pathlib import Path
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from algo.Levenshtein import distance as levenshtein_distance

json_path = Path(__file__).parent.parent / 'static' / 'mygo.json'

with json_path.open('r', encoding='utf-8') as f:
    data = json.load(f)

url = 'https://drive.miyago9267.com/d/file/img/mygo/'
all_pics = all_file.file_list

fuzzy_replacements = {
    "你": ["妳"],
    "妳": ["你"],
    "他": ["她"],
    "她": ["他"],
    "欸": ["耶"],
    "耶": ["欸"],
}

def generate_fuzzy_variants(keyword):
    variants = {keyword}
    for i, char in enumerate(keyword):
        if char in fuzzy_replacements:
            for replacement in fuzzy_replacements[char]:
                new_variant = keyword[:i] + replacement + keyword[i+1:]
                variants.add(new_variant)
    return variants

def calculate_score(keyword, text):
    if keyword == text:
        return 15  # 提高完全匹配時的分數

    score = 0
    if keyword in text:
        score += 5  # 降低包含子字串時的基礎分數，特別是短關鍵字

    max_continuous_match = 0
    for i in range(len(keyword)):
        for j in range(i + 1, len(keyword) + 1):
            if keyword[i:j] in text:
                max_continuous_match = max(max_continuous_match, j - i)

    if max_continuous_match > 1:
        score += max_continuous_match

    return score

def get_pic(keywords: list[str], fuzzy: bool = True):
    scored_results = []
    full_match_results = []

    for item in all_pics:
        name = item['name']
        total_score = 0
        keyword_fully_matched = True

        # 原有算法
        for keyword in keywords:
            fuzzy_variants = generate_fuzzy_variants(keyword) if fuzzy else {keyword}
            max_score_for_keyword = 0
            keyword_matched = False

            for variant in fuzzy_variants:
                if not fuzzy:
                    if variant in name:
                        max_score_for_keyword = 15  # 完全匹配情況下的高分
                        keyword_matched = True
                        break
                else:
                    if variant in name:
                        max_score_for_keyword = max(max_score_for_keyword, 10)  # 如果是部分匹配
                        keyword_matched = True
                    elif len(variant) > 2 and len(name) > 2 and levenshtein_distance(variant, name) <= 2:
                        similarity_ratio = (len(variant) - levenshtein_distance(variant, name)) / len(variant)
                        if similarity_ratio >= 0.5 and variant in name:
                            max_score_for_keyword = max(max_score_for_keyword, 3)  # 相似度較低的情況下給較低的分數
                            keyword_matched = True

            if max_score_for_keyword > 0:
                total_score += max_score_for_keyword
            else:
                keyword_fully_matched = False
                break

        if total_score > 0:
            scored_results.append({'url': url + item['file_name'], 'alt': item['name'], 'score': total_score})

        # 自定義映射邏輯，符合任何關鍵字直接給滿分
        for keyword in keywords:
            if keyword in name:
                full_match_results.append({'url': url + item['file_name'], 'alt': item['name'], 'score': 15})
                break

    # 合併原有算法結果和自定義映射結果，去重
    combined_results = {f"{r['url']}": r for r in (scored_results + full_match_results)}.values()
    sorted_results = sorted(combined_results, key=lambda x: x['score'], reverse=True)

    return JSONResponse(status_code=200, content={'urls': [r for r in sorted_results]})
