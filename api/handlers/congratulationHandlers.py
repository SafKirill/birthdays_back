from logging import getLogger
from uuid import UUID

from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.actions.auth import get_current_user_from_token
from api.actions.congratulation import _create_new_congratulation, _get_congratulation_by_id, _update_congratulation, _get_all_congratulation_is_followed, _get_all_congratulation_is_sender
from api.schemas.schemasCongratulation import CreateCongratulation, ShowCongratulation, ShowListCongratulation, UpdateCongratulationRequest, UpdatedCongratulationResponse
from db.models import User
from db.session import get_db

logger = getLogger(__name__)

congratulation_router = APIRouter()



@congratulation_router.post("/congratulation", response_model=ShowCongratulation)
async def create_user(body: CreateCongratulation, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user_from_token)) -> ShowCongratulation:
    try:
        return await _create_new_congratulation(body=body, sender_id=current_user.id, session=db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")

@congratulation_router.get("/congratulation", response_model=ShowCongratulation)
async def get_user_by_id(congratulation_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user_from_token)) -> ShowCongratulation:
    try:
        user = await _get_congratulation_by_id(congratulation_id, db)
        if user is None:
            raise HTTPException(
                status_code=404, detail=f"Congratulation with id {congratulation_id} not found."
            )
        return user
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")

@congratulation_router.patch("/congratulation", response_model=UpdatedCongratulationResponse)
async def update_user_by_id(congratulation_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user_from_token)) -> UpdatedCongratulationResponse:
    try:
        result = await _update_congratulation(
            congratulation_id=congratulation_id, session=db
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return result

@congratulation_router.get("/all_congratulation_is_sender", response_model=List[ShowListCongratulation])
async def get_all_congratulation_is_sender(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user_from_token)) -> List[ShowListCongratulation]:
    try:
        congratulations = await _get_all_congratulation_is_sender(user_id=current_user.id, session=db)
        if congratulations is None:
            raise HTTPException(
                status_code=404, detail=f"Congratulation not found."
            )
        return congratulations
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")

@congratulation_router.get("/all_congratulation_is_followed", response_model=List[ShowListCongratulation])
async def get_all_congratulation_is_followed(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user_from_token)) -> List[ShowListCongratulation]:
    try:
        congratulations = await _get_all_congratulation_is_followed(user_id=current_user.id, session=db)
        if congratulations is None:
            raise HTTPException(
                status_code=404, detail=f"Congratulation not found."
            )
        return congratulations
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")