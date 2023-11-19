from time import sleep

import psycopg2
from fastapi import Depends, FastAPI, HTTPException, Response, status

# from fastapi.encoders import jsonable_encoder
from psycopg2.extras import RealDictCursor  # Return a col_name as a key in a dict
from sqlalchemy.orm import Session

from . import models, schemas, utils
from .database import engine, get_db

from .routers import post, user

# Create the database tables if they don't exist
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


app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
