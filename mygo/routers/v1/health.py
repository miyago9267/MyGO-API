"""GET /api/v1/health - 健康檢查端點"""
from datetime import datetime

async def health_check():
    """
    健康檢查端點
    
    返回服務狀態和基本資訊
    """
    return {
        'status': 'ok',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'service': 'MyGO API',
        'version': '1.0.0'
    }
