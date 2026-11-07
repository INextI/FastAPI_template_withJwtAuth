from fastapi import APIRouter, Depends
from core.models import db_helper, User, Post
from core.schemas.user import UserBase, UserCreate, UserGet, UserCreateResponse, UserLogin
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from core.depend_session import DependSession
from core.schemas.token import Token
from fastapi import Response, HTTPException, Request
from crud import user as usercrud
from .utils import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    decode_refresh_token,
    validate_password
)
from .cookie import SetTokenCookie
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from .dependencies import DependCurrUser

oauth_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post('/login', response_model=Token)
async def login(user_in: Annotated[OAuth2PasswordRequestForm, Depends()],
                session: AsyncSession,
                response: Response
                ):
    user: User =  await usercrud.get_user_by_email(email=user_in.username, session=session)
    if user is None:
        raise HTTPException(status_code=404, detail="User not registered")

    if not validate_password(password=user_in.password, hashed_password=user.hashed_password):
        raise HTTPException(status_code=401, detail="Wrong password")

    data = {"id": user.id}
    access_token = create_access_token(data_in=data)
    refresh_token = create_refresh_token(data_in=data)
    SetTokenCookie(token=refresh_token).update_response(response=response)

    return {
        "access_token" : access_token
    }

@router.post('/register', response_model=Token)
async def register(user_in: UserCreate,
                   session: AsyncSession,
                   response: Response):
    user = await usercrud.get_user_by_email(email=user_in.email, session=session)
    if user is not None:
        raise HTTPException(status_code=409, detail="User with this email alredy exsist!")

    user: User = usercrud.create_user(user_create=user_in, session=session)
    data = {'id' : user.id}
    access_token = create_access_token(data_in=data)
    refresh_token = create_refresh_token(data_in=data)
    SetTokenCookie(token = refresh_token).update_response(response=response)
    return {
        "access_token" : access_token
    }

@router.post('/logout')
async def logout(response: Response,
                 token: Annotated[str, Depends(oauth_scheme)]
                 ):
    SetTokenCookie.delete_cookie_from_response(response=response)
    return {"message" : "Logout success"}

@router.post('/refresh')
async def get_new_acess_token(request: Request):
    try:
        refresh_token = request.cookies.get('refresh_token')

        if not refresh_token:
            raise HTTPException(status_code=404, detail="Not login!")
        
        dict_in_refresh_token = decode_refresh_token(refresh_token)
        user_id = dict_in_refresh_token.get('id')

        if user_id is None:
            raise HTTPException(status_code=404, detail= "wrong refresh cookie, relogin")

        new_access_token =  create_access_token({'id': user_id})

        return {
            'access_token' : new_access_token
        }
    except Exception:
        raise HTTPException(status_code=401, detail='Unauthorized')

@router.get('/me', response_model=UserGet)
async def get_me(user: DependCurrUser):
    return user