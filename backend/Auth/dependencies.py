from core.models import User
from fastapi import Depends
from typing import Annotated
from .routes import oauth_scheme
from core.depend_session import DependSession
from .utils import decode_access_token
from crud import user as usercrud
from fastapi import HTTPException

async def get_curr_user(token: Annotated[str, Depends(oauth_scheme)],
                        session: DependSession
                        ):
    dict_in_access_token: dict = decode_access_token(token=token)
    
    user_id = dict_in_access_token.get('id')
    if user_id is None:
        raise HTTPException(status_code=404, detail= "wrong access cookie, relogin")

    user: User = await usercrud.get_user_by_id(user_id, session=session)

    if user is None:
        raise HTTPException(status_code=404, detail="This user dont exsist!")
    
    return user

DependCurrUser = Annotated[User, Depends(get_curr_user)]