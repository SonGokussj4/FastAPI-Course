from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create a database URL
SQLALCHEMY_DATABASE_URL = "postgresql://<user>:<password>@<host_or_IP>/<database_name>"

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
