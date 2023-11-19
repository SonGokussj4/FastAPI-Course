from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostPut(PostBase):
    title: str
    content: str

    class Config:
        json_schema_extra = {
            "example": {
                "title": "title1",
                "content": "content1",
                "published": True,
                # "rating": 5,
                # "author": {"name": "author1", "email": "author@gmail.com"},
            }
        }


# ==============
# Response Model
# ==============
class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
