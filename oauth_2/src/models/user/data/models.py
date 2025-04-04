from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str | None = None


class User_model(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone_number: PhoneNumber | None = None
    disabled: bool | None = None

class UserVerify(User_model):
    hashed_password: str

class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone_number: PhoneNumber | None = None
    disabled: bool | None = None
    password: str

class Event(BaseModel):
    user_id: int
    time_start: str
    time_end: str
    description: str
    tags: list[str]
    place: str