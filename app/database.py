from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# Create a database URL
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://"
    f"{settings.database_username}:{settings.database_passport}@"
    f"{settings.database_hostname}:{settings.database_port}/"
    f"{settings.database_name}"
)

# Create an engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class, this will be inherited by all the models
Base = declarative_base()


# Everytime we get a request, we will create a new session and then close it after the request is done
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


### For reference ###
# import psycopg2
# from psycopg2.extras import RealDictCursor  # Return a col_name as a key in a dict
# from time import sleep
# while True:
#     try:
#         conn = psycopg2.connect(
#             host="130.61.176.96",
#             port=5432,
#             database="fastapidb",
#             user="postgres",
#             password="matrix",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print("Connected to the database")
#         break
#     except Exception as e:
#         print("Failed to connect to the database")
#         print("Error: ", e)
#         sleep(5)
