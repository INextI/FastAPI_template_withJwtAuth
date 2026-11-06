from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends
from core.models import db_helper

DependSession = Annotated[AsyncSession, Depends(db_helper.session_getter)]