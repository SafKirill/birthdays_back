from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from typing import List
from sqlalchemy.orm import selectinload
from db.models import Congratulation, User

class CongratulationDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_congratulation(self, sender_id: UUID, receiver_id: UUID, message: str) -> Congratulation:
        receiver = await self.db_session.get(User, receiver_id)
        if not receiver:
            raise ValueError(f"User with id {receiver_id} does not exist.")

        sender = await self.db_session.get(User, sender_id)
        if not sender:
            raise ValueError(f"User with id {sender_id} does not exist.")

        new_congratulation = Congratulation(
            sender_id=sender_id,
            receiver_id=receiver_id,
            message=message,
        )
        self.db_session.add(new_congratulation)
        await self.db_session.flush()
        await self.db_session.refresh(new_congratulation)

        return new_congratulation, sender, receiver

    async def get_congratulation_by_id(self, congratulation_id: UUID) -> Congratulation:
        congratulation = await self.db_session.execute(
            select(Congratulation)
            .options(
                selectinload(Congratulation.sender),
                selectinload(Congratulation.receiver)
            )
            .filter(Congratulation.id == congratulation_id)
        )
        congratulation = congratulation.scalar_one()
        return congratulation

    async def update_congratulation(self, congratulation_id: UUID) -> Congratulation:
        stmt = (
            update(Congratulation)
            .where(Congratulation.id == congratulation_id)
            .values(is_read=True)
            .execution_options(synchronize_session="fetch")
        )
        await self.db_session.execute(stmt)

        stmt = (
            select(Congratulation)
            .where(Congratulation.id == congratulation_id)
            .options(
                selectinload(Congratulation.sender),
                selectinload(Congratulation.receiver)
            )
        )
        result = await self.db_session.execute(stmt)
        congratulation = result.scalar_one()

        return congratulation

    async def get_all_congratulation_is_sender(self, user_id: UUID) -> List[Congratulation]:
        stmt = select(Congratulation).where(Congratulation.sender_id == user_id)
        result = await self.db_session.execute(
            stmt.options(
                selectinload(Congratulation.sender),
                selectinload(Congratulation.receiver)
            )
        )
        congratulations = result.scalars().all()
        return congratulations

    async def get_all_congratulation_is_followed(self, user_id: UUID) -> List[Congratulation]:
        stmt = select(Congratulation).where(Congratulation.receiver_id == user_id)
        result = await self.db_session.execute(
            stmt.options(
                selectinload(Congratulation.sender),
                selectinload(Congratulation.receiver)
            )
        )
        congratulations = result.scalars().all()
        return congratulations