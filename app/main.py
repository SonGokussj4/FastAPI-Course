from time import sleep

import psycopg2
from fastapi import Depends, FastAPI, HTTPException, Response, status

# from fastapi.encoders import jsonable_encoder
from psycopg2.extras import RealDictCursor  # Return a col_name as a key in a dict
from sqlalchemy.orm import Session

from . import models, schemas, utils
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts", response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )
    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())  # Create a new post
    db.add(new_post)  # Add it to the database
    db.commit()  # Commit the changes to the database
    db.refresh(new_post)  # "Retrieve" the post from the db and store it in the var
    return new_post


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()


# @app.patch("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
# def update_patch_post(id: int, post: schemas.PostCreate):
#     # Official FastAPi solution
#     stored_item_data = my_posts[id]
#     if stored_item_data is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with id: {id} was not found",
#         )

#     stored_item_model = schemas.PostCreate(**stored_item_data)
#     update_data = post.model_dump(exclude_unset=True)
#     updated_item = stored_item_model.model_copy(update=update_data)
#     my_posts[id] = jsonable_encoder(updated_item)
#     return updated_item


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
