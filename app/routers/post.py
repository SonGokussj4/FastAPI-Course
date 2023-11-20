from fastapi import Depends, status, HTTPException, APIRouter, Response
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db

# @app.get --> @router.get
router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


@router.get("/", response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)
):
    new_post = models.Post(**post.model_dump())  # Create a new post
    db.add(new_post)  # Add it to the database
    db.commit()  # Commit the changes to the database
    db.refresh(new_post)  # "Retrieve" the post from the db and store it in the var
    return new_post


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):
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


# @router.patch("/{id}", status_code=status.HTTP_202_ACCEPTED)
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


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
