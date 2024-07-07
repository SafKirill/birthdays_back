from uuid import UUID
from sqlalchemy import delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Follow

class FollowDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_follow(self, follower_id: UUID, followed_id: UUID) -> Follow:
        new_follow = Follow(
            follower_id=follower_id,
            followed_id=followed_id,
        )
        self.db_session.add(new_follow)
        await self.db_session.flush()
        await self.db_session.refresh(new_follow)
        return new_follow

    async def remove_follow(self, follower_id: UUID, followed_id: UUID):
        query = delete(Follow).where(and_(Follow.follower_id == follower_id, Follow.followed_id == followed_id))
        await self.db_session.execute(query)