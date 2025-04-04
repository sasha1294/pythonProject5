from fastapi import HTTPException, Depends
import jwt
from datetime import datetime, timedelta, timezone

from passlib.exc import InvalidTokenError
from starlette import status
from oauth_2.src.models.user.data.tools import get_user
from oauth_2.env.env import SECRET_KEY, ALGORITHM
from oauth_2.src.models.user.data.models import TokenData, User_model
from oauth_2.src.conf.Api_conf import oauth2_scheme
from typing import Annotated

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("sub")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(id=token_data.id)
    if user == False:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User_model, Depends(get_current_user)],
):
    if current_user["disabled"]:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def image_converter():
    pass