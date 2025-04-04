from sqlalchemy import String, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from oauth_2.src.conf.Alchemy_conf import Base
from typing import List

class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column()
    disable: Mapped[bool] = mapped_column()

class Event(Base):
    __tablename__ = 'event'

    img: Mapped[bytes] = mapped_column()
    user_id: Mapped[int] = mapped_column(nullable=False)
    event_id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    time_start: Mapped[str] = mapped_column(DateTime, nullable=False)
    time_end: Mapped[str] = mapped_column(DateTime, nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    tags: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    place: Mapped[str] = mapped_column(nullable=False)

