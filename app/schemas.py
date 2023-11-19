from typing import Optional

from pydantic import BaseModel


class Author(BaseModel):
    name: str
    email: Optional[str] = None


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None
    # author: Optional["Author"] = None


class PostBase(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
    # rating: Optional[int] = None
    # author: Optional["Author"] = None


class PostPatch(PostBase):
    ...


class PostPut(PostBase):
    title: str
    content: str

    class Config:
        json_schema_extra = {
            "example": {
                "title": "title1",
                "content": "content1",
                "published": True,
                "rating": 5,
                "author": {"name": "author1", "email": "author@gmail.com"},
            }
        }
