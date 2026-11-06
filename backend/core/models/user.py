from sqlalchemy.orm import  Mapped, mapped_column, relationship
from .base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .post import Post

class User(Base):
    first_name: Mapped[str]
    second_name: Mapped[str]
    avatar_img: Mapped[str]
    hashed_password: Mapped[bytes]
    nickname: Mapped[str]
    email: Mapped[str] = mapped_column(unique= True)

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user", cascade="all, delete-orphan")