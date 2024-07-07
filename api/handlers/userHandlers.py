from logging import getLogger
from typing import List, Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.actions.auth import get_current_user_from_token
from api.actions.user import _create_new_user, _get_all_users, _get_user_by_id, _update_user
from api.schemas.schemasUser import CreateUser, ShowUser, ShowAllUsers, UpdateUserRequest, UpdatedUserResponse, ShowUserInfo
from db.models import User
from db.session import get_db

logger = getLogger(__name__)

user_router = APIRouter()



@user_router.post("/user", response_model=ShowUser)
async def create_user(body: CreateUser, db: AsyncSession = Depends(get_db)) -> ShowUser:
    try:
        return await _create_new_user(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@user_router.patch("/user", response_model=UpdatedUserResponse)
async def update_user_by_id(body: UpdateUserRequest, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user_from_token)) -> UpdatedUserResponse:
    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for user update info should be provided",
        )
    try:
        updated_user_id = await _update_user(
            updated_user_params=updated_user_params, session=db, user=current_user
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatedUserResponse(updated_user_id=updated_user_id)

@user_router.get("/user", response_model=ShowUserInfo)
async def get_user(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user_from_token)) -> ShowUserInfo:
    try:
        return await _get_user_by_id(user_id=current_user.id, session=db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")

@user_router.get("/all_user", response_model=List[ShowAllUsers])
async def get_all_users(name: Optional[str] = None, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user_from_token)) -> List[ShowAllUsers]:
    try:
        return await _get_all_users(user_id=current_user.id, name=name, session=db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")