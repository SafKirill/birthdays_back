from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User
from db.dals.followDal import FollowDAL
from db.dals.alertDal import AlertDAL
from api.schemas.schemasFollow import ShowFollow



async def _create_new_follow(user: User, followed_id:UUID, session: AsyncSession) -> ShowFollow:
    async with session.begin():
        follow_dal = FollowDAL(session)
        follow = await follow_dal.create_follow(
            follower_id=user.id,
            followed_id=followed_id,
        )
        alert_dal = AlertDAL(session)
        await alert_dal.create_or_update_alerts(user=user)
        return ShowFollow(
            id=follow.id,
        )


async def _remove_follow(follower_id: UUID, followed_id: UUID, session: AsyncSession) -> bool:
    async with session.begin():
        follow_dal = FollowDAL(session)
        alert_dal = AlertDAL(session)

        await follow_dal.remove_follow(follower_id=follower_id, followed_id=followed_id)
        await alert_dal.remove_alert(follower_id=follower_id, followed_id=followed_id)

    await session.commit()
    return True