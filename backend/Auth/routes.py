from fastapi import APIRouter, Depends
from core.models import db_helper, User, Post
from core.schemas.user import UserBase, UserCreate, UserGet, UserCreateResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from core.depend_session import DependSession
from core.schemas.token import Token
from fastapi import Response, HTTPException
from crud import user as usercrud
from .utils import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    decode_refresh_token
)
from .cookie import SetTokenCookie

router = APIRouter(prefix="", tags=["Auth"])

@router.post('/login')
async def login():
    pass

@router.post('/register', response_model=Token)
async def register(user_in: UserCreate,
                   session: AsyncSession,
                   response: Response):
    user = usercrud.get_user_by_email(email=user_in.email, session=session)
    if user is not None:
        raise HTTPException(status_code=409, detail="This user alredy exsist!")

    user: User = usercrud.create_user(user_create=user_in, session=session)
    data = {'id' : user.id}
    access_token = create_access_token(data_in=data)
    refresh_token = create_refresh_token(data_in=data)
    SetTokenCookie(token = refresh_token).update_response(response=response)
    return {
        "AccessToken" : access_token
    }

@router.post('/logout')
async def logout():
    pass

@router.post('/access')
async def get_access_token():
    pass

@router.post('/refresh')
async def get_refresh_token():
    pass

@router.get('/me')
async def get_me():
    pass