"""Main server file for FastAPI application."""
import os
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from routers import mygo
from routers.v1 import router as v1_router
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

origins = [
    'http://localhost:4000',
    'https://mygo.miyago9267.com',
    'https://mygotest.miyago9267.com',
    '*'
]

app = FastAPI(
    title="MyGO API",
    description="API for MyGO meme picture library",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# V1 API routes (新版 API)
app.include_router(
    v1_router,
    prefix="/api/v1",
    tags=["V1"]
)

# Legacy routes (向後相容)
app.include_router(
    mygo.router,
    prefix="/mygo",
    tags=["Legacy MyGo"]
)

@app.get('/PING', tags=["Health"])
def ping() -> str:
    """Return testing PONG"""
    return 'PONG'

@app.get('/api/ping', tags=["Health"])
def api_ping() -> dict:
    """Return API ping response"""
    return {'message': 'pong'}

if __name__ == "__main__":
    uvicorn.run(
        'app:app',
        host='0.0.0.0',
        port=int(os.getenv("SERVER_PORT",'3030')),
        reload=True
    )