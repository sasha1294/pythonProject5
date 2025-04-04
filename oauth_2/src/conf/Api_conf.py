from authlib.integrations.starlette_client import OAuth
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from oauth_2.env.env import middleware_sicret_key, client_id, clientSecret

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8000/Oauth2/token")
template = Jinja2Templates(directory="templates")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")

oauth = OAuth()
oauth.register(
    name= "google",
    server_metadata_url= "https://accounts.google.com/.well-known/openid-configuration",
    client_secret=clientSecret,
    client_id=client_id,
    client_kwargs={
        "scope": "email openid profile",
        "redirect_url": "http://localhost:8000/Oauth2/auth"
    }
)

origins = [
    "http://localhost:8000",
]

app.add_middleware(SessionMiddleware, secret_key=middleware_sicret_key)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


