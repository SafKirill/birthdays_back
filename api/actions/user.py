from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from hashing import Hasher
from db.dals.userDal import UserDAL
from db.dals.alertDal import AlertDAL
from db.models import User
from api.schemas.schemasUser import CreateUser, ShowUser, ShowAllUsers, ShowUserInfo

async def _create_new_user(body: CreateUser, session: AsyncSession) -> ShowUser:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(
            fullname=body.fullname,
            hashed_password=Hasher.get_password_hash(body.password),
            date_of_birthday=body.date_of_birthday,
            email=body.email,
        )
        return ShowUser(
            id=user.id,
            fullname=user.fullname,
            date_of_birthday=user.date_of_birthday,
        )

async def _update_user(updated_user_params: dict, user: User, session) -> Optional[UUID]:
    async with session.begin():
        user_dal = UserDAL(session)
        updated_user_id = await user_dal.update_user(
            user_id=user.id, **updated_user_params
        )
        alert_dal = AlertDAL(session)
        await alert_dal.create_or_update_alerts(user=user)

        return updated_user_id.id

async def _get_all_users(user_id: UUID, name: str, session: AsyncSession) -> Optional[List[ShowAllUsers]]:
    async with session.begin():
        user_dal = UserDAL(session)
        all_users = await user_dal.get_all_users(user_id=user_id, name=name)
        return all_users

async def _get_user_by_id(user_id: UUID, session: AsyncSession) -> ShowUserInfo:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_id(user_id=user_id)
        return ShowUserInfo(
            days_before_birthday_alert=user.days_before_birthday_alert,
        )
async def _get_user_by_email_for_auth(email: str, session: AsyncSession):
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_email(email=email)
        return user