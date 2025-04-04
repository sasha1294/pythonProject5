from oauth_2.src.conf.Alchemy_conf import Session
from oauth_2.src.models.user.data.user_shema import User, Event
from sqlalchemy import select, insert
from datetime import datetime

async def userCreate(data):
    async with Session() as session:
        await session.execute(insert(User).values(username=data["username"], password=data["password"],
                                   email=data["email"], phone_number=data["phone"],
                                   disable=False))

        await session.commit()

async def eventCreate(img: bytes, user_id: int, time_start: datetime, time_end:datetime,  description:str,
                      tags: list[str], place: str, name: str):
    async with Session() as session:
        await session.execute(insert(Event).values(img=img, name=name, user_id=user_id, time_start=time_start,
                                                   time_end=time_end,  description= description, tags=tags,
                                                   place=place))
        await session.commit()

async def authenticate_user(username: str, password: str):
    async with Session() as session:
        result = await session.execute(select(User).where(User.username == username).where(User.password == password))
        user = result.scalars().all()

        if user is None:
            return False

        else:
            return str(user[0].id)


async def get_user(id: str):
    async with Session() as session:
        user_data = await session.execute(select(User).where(User.id == int(id)))
        user = user_data.scalars().all()

        if user is None:
            return False

        else:
            return {"id": user[0].id,
                    "username": user[0].username,
                    "email": user[0].email,
                    "phone_number": user[0].phone_number,
                    "disabled": user[0].disable}

async def get_event_tag(tag: list[str]):
    async with Session() as session:
        event_data = await session.execute(select(Event).where(Event.tags == tag))
        event = event_data.scalars().all()

        if event is None:
            return False

        else:
            return event

async def get_event_name(name: str):
    async with Session() as session:
        event_data = await session.execute(select(Event).where(Event.name == name))
        event = event_data.scalars().all()

        if event is None:
            return False

        else:
            return event