from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Author(BaseModel):
    name: str
    email: Optional[str] = None


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    author: Optional["Author"] = None


my_posts: list[dict] = [
    {"title": "title1", "content": "content1", "id": 1},
    {"title": "title2", "content": "content2", "id": 2},
]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts")
def create_posts(new_post: Post):
    print("new_post")
    print(new_post.dict())
    return {"new_post": f"title: '{new_post.title}' content: '{new_post.content}'"}
