from sqlalchemy.ext.asyncio import AsyncSession
from core.models import User
from sqlalchemy import select
from sqlalchemy.engine import Result
from core.schemas.user import UserCreate, UserGet
from Auth.utils import hashed_password, validate_password
from core.config import settings

async def get_user_by_id(user_id: int, session: AsyncSession) -> User | None:
    stmt = select(User).filter_by(id = user_id)
    result: Result = await session.execute(stmt)
    user: User | None = result.scalar_one_or_none()
    return user

async def create_user(user_create: UserCreate, session: AsyncSession) -> User:
    user: User = User(**user_create.model_dump(exclude="password"))
    user.hashed_password = hashed_password(user_create.password)
    if user.avatar_img is None:
        user.avatar_img = str(settings.deffault_avatar_img)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def get_all_users(session: AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users: list[User] = result.scalars().all()
    return users

async def delete_user_by_id(user_id: int, session: AsyncSession) -> None:
    stmt = select(User).filter_by(id=user_id)
    res: Result = await session.execute(stmt)
    user = res.scalar_one_or_none()
    await session.delete(user)
    await session.commit()


async def get_user_by_email(email: str, session: AsyncSession) -> User:
    stmt = select(User).filter_by(email=email)
    res : Result = await session.execute(stmt)
    user = res.scalar_one_or_none()
    return user
