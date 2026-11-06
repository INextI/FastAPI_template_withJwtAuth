from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from sqlalchemy import ForeignKey

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User

class Post(Base):
    title: Mapped[str]
    text: Mapped[str]
    main_img_url: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))


    user: Mapped["User"] = relationship("User", back_populates="posts")