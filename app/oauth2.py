from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "<really_long_secret_key_ideally_generated_with_a_random_key_generator>"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    data_to_encode = data.copy()

    # Add the expire time to the payload
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({"exp": expire})

    token = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token
