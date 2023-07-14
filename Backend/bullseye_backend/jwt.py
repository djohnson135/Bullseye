import os
from dotenv import load_dotenv
from datetime import datetime
from datetime import timedelta

import jwt
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer

import bullseye_backend.crud.user as crud
from sqlalchemy.orm import Session
from bullseye_backend.dependencies import get_db
from bullseye_backend.database import SessionLocal
import bullseye_backend.models.user as model


API_SECRET_KEY = os.getenv('API_SECRET_KEY') or None
API_ALGORITHM = os.getenv('API_ALGORITHM') or 'HS256'
# API_ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('API_ACCESS_TOKEN_EXPIRE_MINUTES') or 15


if API_SECRET_KEY is None:
    raise BaseException('Missing API_SECRET_KEY env var.')

# Helper to read numbers using var envs
def cast_to_number(id):
    temp = os.getenv(id)
    if temp is not None:
        try:
            return float(temp)
        except ValueError:
            return None
    return None

API_ACCESS_TOKEN_EXPIRE_MINUTES = cast_to_number('API_ACCESS_TOKEN_EXPIRE_MINUTES') or 15


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')


# Error
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)

# Create token internal function
def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, API_SECRET_KEY, algorithm=API_ALGORITHM)
    return encoded_jwt


# Create token for an email
def create_token(email):
    access_token_expires = timedelta(minutes=API_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub': email}, expires_delta=access_token_expires)
    return access_token


def valid_email_from_db(email):
    db = SessionLocal()
    user = db.query(model.User).filter_by(email = email).first()
    if user is None:
        return False
    return True

async def get_current_user_email(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, API_SECRET_KEY, algorithms=[API_ALGORITHM])
        email: str = payload.get('sub')
        if email is None:
            raise CREDENTIALS_EXCEPTION
    except jwt.PyJWTError:
        raise CREDENTIALS_EXCEPTION

    if valid_email_from_db(email):
        return email

    raise CREDENTIALS_EXCEPTION