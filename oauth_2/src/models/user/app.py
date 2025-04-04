from datetime import timedelta, datetime
from typing import Annotated

from authlib.integrations.base_client import OAuthError
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status, APIRouter, File
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.datastructures import FormData

from oauth_2.env.env import ACCESS_TOKEN_EXPIRE_MINUTES
from oauth_2.src.conf.Alchemy_conf import create_base
from oauth_2.src.models.user.data.models import Token, User_model, User
from oauth_2.src.models.user.data.tools import authenticate_user, userCreate, eventCreate
from oauth_2.src.encrypt.encrypt import create_access_token, get_current_active_user
from oauth_2.src.conf.Api_conf import template
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/example")

@router.get("/event")
async def main_page(request: Request):
    return template.TemplateResponse(name="inf.html", context={"request": request})

@router.get("/in")
async def main_page(request: Request):
    return template.TemplateResponse(name="logn.html", context={"request": request})

@router.get("/register_in")
async def user_acc(request: Request):
    return template.TemplateResponse(name="reg.html", context={"request": request})

@router.get("/main")
async def client_main(request: Request):
    return template.TemplateResponse(name="main_page.html", context={"request": request})

@router.get("/user_ac")
async def calendar(request: Request):
    return template.TemplateResponse(name="user.html", context={"request": request})

@router.post("/dev_event")
async def dev_event(file: Annotated[bytes, File()], time_start: datetime, time_end: datetime,
                    description: str, tags: list[str], place: str, name:str,
                    current_user: Annotated[User_model, Depends(get_current_active_user)]):
    try:
        id = current_user.id
        await create_base()
        await eventCreate(time_start=time_start, time_end=time_end,
                          description=description, tags=tags, place=place,
                          img=file, user_id=id, name=name)
        return {"ok": "dfghh"}

    except Exception as e:
        raise HTTPException(status_code=401, detail={"error": e})


@router.post("/register")
async def register_user(request: Request):
    try:
        user_data = dict(await request.form())
        await userCreate(data=user_data)
        return RedirectResponse(status_code=303, url="/example/main")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Registration failed: {str(e)}"
        )




@router.get("/main")
async def main_page(request: Request):
    return template.TemplateResponse(name="main_page.html", context={"request": request})


#google
"""
@router.get("/create_ac")
async def registration(request: Request):
    try:
        url = request.url_for("auth")
        return await oauth.google.authorize_redirect(request, url)

    except ValueError:
        return "unauthorized"

@router.get('/auth')
async def auth(request: Request):
    try:
       token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        return JSONResponse(content={"error": str(e)})

    user_data = token.get("userinfo")
    if user_data:
        request.session["user"] = dict(user_data)
        await create_base()
        await userCreate(user_data)
    return RedirectResponse(url="example/user_ac", status_code=303)
"""

#oauth2
@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if user == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

