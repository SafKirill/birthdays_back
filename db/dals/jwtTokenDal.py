from typing import Optional
from uuid import UUID
import datetime
from sqlalchemy import and_, select, delete
from sqlalchemy.ext.asyncio import AsyncSession


import db.models as models


class JwtTokenDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_jwt_token(self, user_id: UUID, jwt: str, client_id: str, date_of_creation: datetime.datetime = datetime.datetime.utcnow()) -> models.JwtToken:
        new_jwt_token = models.JwtToken(
            user_id=user_id,
            jwt=jwt,
            date_of_creation=date_of_creation,
            client_id=client_id,
        )
        self.db_session.add(new_jwt_token)
        await self.db_session.flush()
        await self.db_session.refresh(new_jwt_token)
        return new_jwt_token

    async def delete_jwt_token(self, jwt_token_id: UUID) -> Optional[bool]:
        query = (
            delete(models.JwtToken).where(and_(models.JwtToken.id == jwt_token_id, models.JwtToken.is_active == True))
        )
        await self.db_session.execute(query)
        return True

    async def delete_jwt_token_by_jwt(self, jwt_token: str) -> Optional[bool]:
        query = (
            delete(models.JwtToken).where(and_(models.JwtToken.jwt == jwt_token, models.JwtToken.is_active == True))
        )
        await self.db_session.execute(query)
        return True

    async def get_jwt_token_by_user_id(self, user_id: UUID, client_id: str) -> Optional[models.JwtToken]:
        query = select(models.JwtToken).where(and_(models.JwtToken.user_id == user_id, models.JwtToken.is_active == True, models.JwtToken.client_id == client_id))
        res = await self.db_session.execute(query)
        jwt_token_row = res.fetchone()
        if jwt_token_row is not None:
            return jwt_token_row[0]

    async def get_jwt_token_by_id(self, jwt_token_id: UUID) -> Optional[models.JwtToken]:
        query = select(models.JwtToken).where(and_(models.JwtToken.id == jwt_token_id, models.JwtToken.is_active == True))
        res = await self.db_session.execute(query)
        jwt_token_row = res.fetchone()
        if jwt_token_row is not None:
            return jwt_token_row[0]

    async def check_jwt_token(self, user_id: UUID, jwt_token: str):
        query = select(models.JwtToken).where(and_(models.JwtToken.user_id == user_id, models.JwtToken.jwt == jwt_token, models.JwtToken.is_active == True))
        res = await self.db_session.execute(query)
        jwt_token_row = res.fetchone()
        if jwt_token_row is not None:
            return True
        else:
            return False