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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}


@app.post("/createposts")
def create_posts(new_post: Post):
    print("new_post")
    print(new_post.dict())
    return {"new_post": f"title: '{new_post.title}' content: '{new_post.content}'"}
