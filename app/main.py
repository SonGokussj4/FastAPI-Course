from random import randrange
from time import sleep
from typing import Optional

import psycopg2
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder

# This will return a column name as a key in a dictionary
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

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


@app.get("/sqlalchemy")
def get_sqlalchemy_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * from posts WHERE id = %s""", (id,))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )

    return {"data": post}


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_put_post(id: int, post: PostPut):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
        (post.title, post.content, post.published, id),
    )

    updated_post = cursor.fetchone()

    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )

    conn.commit()
    return {"data": updated_post}


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
    # post = find_post(id)
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    deleted_post = cursor.fetchone()

    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )

    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
