"""Main server file for FastAPI application."""
import os
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from routers import mygo
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

origins = [
    'http://localhost:4000',
    'https://mygo.miyago9267.com',
    'https://mygotest.miyago9267.com',
    '*'
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(
    mygo.router,
    prefix="/mygo",
    tags=["MyGo"]
)

@app.get('/PING')
def ping() -> str:
    """Return tesing PONG"""
    return 'PONG'

if __name__ == "__main__":
    uvicorn.run(
        'app:app',
        host='0.0.0.0',
        port=int(os.getenv("SERVER_PORT",'3030')),
        reload=True
    )