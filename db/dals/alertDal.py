from uuid import UUID
from datetime import date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import delete, and_, update, func
from typing import List
from db.models import Follow
from db.models import User
from db.models import Alert

class AlertDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_or_update_alerts(self, user: User):
        result = await self.db_session.execute(
            select(Follow).filter(Follow.follower_id == user.id)
        )
        followed_users = result.scalars().all()

        for follow in followed_users:
            followed_user_result = await self.db_session.execute(
                select(User).filter(User.id == follow.followed_id).options(selectinload(User.followers))
            )
            followed_user = followed_user_result.scalar_one()
            alert_date = followed_user.date_of_birthday.replace(year=date.today().year) - timedelta(
                days=user.days_before_birthday_alert)

            # Проверяем, если день рождения уже прошел в этом году
            if alert_date < date.today():
                alert_date = alert_date.replace(year=alert_date.year + 1)

            # Проверяем, существует ли уже оповещение
            existing_alert_result = await self.db_session.execute(
                select(Alert).filter(
                    Alert.user_id == user.id,
                    Alert.followed_user_id == followed_user.id
                )
            )
            existing_alert = existing_alert_result.scalar_one_or_none()

            if existing_alert:
                # Обновляем существующее оповещение
                existing_alert.alert_date = alert_date
                existing_alert.days_before_birthday = user.days_before_birthday_alert
            else:
                # Создаем новое оповещение
                alert = Alert(
                    user_id=user.id,
                    followed_user_id=followed_user.id,
                    alert_date=alert_date,
                    days_before_birthday=user.days_before_birthday_alert
                )
                self.db_session.add(alert)

        await self.db_session.commit()

    async def get_alert_by_date(self, date):
        async with self.db_session as session:
            query = select(Alert).filter(Alert.alert_date == date)
            result = await session.execute(query.options(selectinload(Alert.user), selectinload(Alert.followed_user)))
            alerts = result.scalars().all()
            return alerts

    async def update_alert_dates(self, ids: List[UUID]):
        async with self.db_session as session:
            stmt = (
                update(Alert)
                .where(Alert.id.in_(ids))
                .values(alert_date=func.date_trunc('day', Alert.alert_date + timedelta(days=365)))
            )
            try:
                result = await session.execute(stmt)
                await session.commit()
            except Exception as e:
                print(f"Ошибка при обновлении записей: {e}")
                raise

    async def remove_alert(self, follower_id: UUID, followed_id: UUID):
        query = delete(Alert).where(and_(Alert.user_id == follower_id, Alert.followed_user_id == followed_id))
        await self.db_session.execute(query)
