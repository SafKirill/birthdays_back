from logging import getLogger
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.actions.auth import get_current_user_from_token
from api.actions.follow import _create_new_follow, _remove_follow
from api.schemas.schemasFollow import ShowFollow
from db.models import User
from db.session import get_db

logger = getLogger(__name__)

follow_router = APIRouter()

@follow_router.post("/follow", response_model=ShowFollow)
async def create_follow(followed_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user_from_token)) -> ShowFollow:
    try:
        return await _create_new_follow(user=current_user, followed_id=followed_id, session=db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")

@follow_router.delete("/follow", response_model=bool)
async def remove_follow(followed_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user_from_token)) -> bool:
    try:
        return await _remove_follow(follower_id=current_user.id, followed_id=followed_id, session=db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")