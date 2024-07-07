from typing import Optional
from uuid import UUID
from api.schemas.schemasJwtToken import ShowJwtToken
from api.schemas.schemasJwtToken import JwtTokenCreate
from db.dals.jwtTokenDal import JwtTokenDAL

async def _create_new_jwt_token(body: JwtTokenCreate, session) -> ShowJwtToken:
    async with session.begin():
        jwt_token_dal = JwtTokenDAL(session)
        jwt_token = await jwt_token_dal.create_jwt_token(
            user_id=body.user_id,
            jwt=body.jwt,
            date_of_creation=body.date_of_creation,
            client_id=body.client_id
        )
        return ShowJwtToken(
            id=jwt_token.id,
            user_id=jwt_token.user_id,
            jwt=jwt_token.jwt,
            date_of_creation=jwt_token.date_of_creation,
            is_active=jwt_token.is_active,
            client_id=jwt_token.client_id
        )

async def _delete_jwt_token(jwt_token_id: UUID, session):
    async with session.begin():
        jwt_token_dal = JwtTokenDAL(session)
        deleted_jwt_token_id = await jwt_token_dal.delete_jwt_token(
            jwt_token_id=jwt_token_id,
        )
        return deleted_jwt_token_id

async def _delete_jwt_token_by_jwt(jwt_token: str, session):
    async with session.begin():
        jwt_token_dal = JwtTokenDAL(session)
        deleted_jwt_token_id = await jwt_token_dal.delete_jwt_token_by_jwt(
            jwt_token=jwt_token,
        )
        return deleted_jwt_token_id


async def _get_jwt_token_by_user_id(user_id: UUID, client_id: str, session) -> Optional[ShowJwtToken]:
    async with session.begin():
        jwt_token_dal = JwtTokenDAL(session)
        st = await jwt_token_dal.get_jwt_token_by_user_id(
            user_id=user_id,
            client_id=client_id
        )
        if st is not None:
            return st

async def _check_jwt_token(user_id: UUID, jwt_token: str, session):
    async with session.begin():
        jwt_token_dal = JwtTokenDAL(session)
        res = await jwt_token_dal.check_jwt_token(
            user_id=user_id,
            jwt_token=jwt_token
        )
        return res