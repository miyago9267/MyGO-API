from typing import Optional
from pydantic import BaseModel, EmailStr, validator

class Tags(BaseModel):
    name: str
    description: str
    url: str
    tags: list[str]