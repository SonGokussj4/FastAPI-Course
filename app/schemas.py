from typing import Optional

from pydantic import BaseModel


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
