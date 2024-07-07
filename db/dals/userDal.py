import datetime
from typing import Optional, List
from uuid import UUID
from sqlalchemy import update, and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from db.models import User, Follow
from api.schemas.schemasUser import ShowAllUsers
class UserDAL:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, fullname: str, hashed_password: str, email: str, date_of_birthday: datetime.date) -> User:
        new_user = User(
            fullname=fullname,
            hashed_password=hashed_password,
            email=email,
            date_of_birthday=date_of_birthday,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        await self.db_session.refresh(new_user)
        return new_user

    async def get_all_users(self, user_id: UUID, name: Optional[str] = None) -> List[ShowAllUsers]:
        is_following = aliased(Follow)

        query = select(
            User.id,
            User.fullname,
            User.date_of_birthday,
            (is_following.follower_id.isnot(None)).label('signed')
        ).distinct(User.id).outerjoin(
            is_following, (is_following.followed_id == User.id) & (is_following.follower_id == user_id)
        )

        query = query.where(User.id != user_id)

        if name:
            query = query.where(User.fullname.ilike(f"%{name}%"))

        result = await self.db_session.execute(query)

        users = result.all()
        return [
            ShowAllUsers(
                id=user.id,
                fullname=user.fullname,
                date_of_birthday=user.date_of_birthday,
                signed=user.signed
            )
            for user in users
        ]
    async def update_user(self, user_id: UUID, **kwargs) -> Optional[User]:
        query = (
            update(User)
            .where(and_(User.id == user_id, User.is_active == True))
            .values(kwargs).returning(User)
        )
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]

    async def get_user_by_email(self, email: str) -> Optional[User]:
        query = select(User).where(User.email.ilike(email))
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        query = select(User).where(User.id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]
