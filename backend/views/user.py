from fastapi import APIRouter, Depends
from core.models import db_helper, User, Post
from core.schemas.user import UserBase, UserCreate, UserGet, UserCreateResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from core.depend_session import DependSession

from crud import user as usercrud

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get('/', response_model= list[UserGet])
async def get_all_users(session: DependSession):
    return await usercrud.get_all_users(session=session)

@router.get('/{user_id}', response_model=UserGet)
async def get_user(user_id: int, session: DependSession):
    user: User = await usercrud.get_user_by_id(user_id, session)
    return UserGet(user)

@router.post('/', response_model=UserCreateResponse)
async def create_user(user: UserCreate, session: DependSession):
    user = await usercrud.create_user(user, session)
    return user

@router.delete('/{user_id}')
async def delete_user_by_id(user_id: int, session: DependSession):
    await usercrud.delete_user_by_id(user_id= user_id, session = session)
    return {"message" : "Delete succesful"}