from random import randrange
from time import sleep
from typing import Optional

from fastapi import FastAPI, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

import psycopg2
from psycopg2.extras import RealDictCursor  # This will return a column name as a key in a dictionary

app = FastAPI()


class Author(BaseModel):
    name: str
    email: Optional[str] = None


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None
    # author: Optional["Author"] = None


while True:
    try:
        conn = psycopg2.connect(
            host="redacted",
            port=5432,
            database="redacted",
            user="redacted",
            password="redacted",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Connected to the database")
        break
    except Exception as e:
        print("Failed to connect to the database")
        print("Error: ", e)
        sleep(5)


class PostBase(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
    rating: Optional[int] = None
    author: Optional["Author"] = None


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


my_posts: list[dict] = [
    {"title": "title1", "content": "content1", "id": 1},
    {"title": "title2", "content": "content2", "id": 2},
]


def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
    return None


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if post:
        return {"data": post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_put_post(id: int, post: PostPut):
    post_dict = post.model_dump()
    post_dict["id"] = id

    for i, p in enumerate(my_posts):
        if p["id"] == id:
            my_posts[i] = post_dict
            return {"data": post_dict}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")


@app.patch("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_patch_post(id: int, post: PostPatch):
    # Official FastAPi solution
    stored_item_data = my_posts[id]
    if stored_item_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    stored_item_model = PostPatch(**stored_item_data)
    update_data = post.model_dump(exclude_unset=True)
    updated_item = stored_item_model.model_copy(update=update_data)
    my_posts[id] = jsonable_encoder(updated_item)
    return updated_item


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_post(id)
    if post:
        my_posts.remove(post)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
