from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from db.dals.congratulationDal import CongratulationDAL
from api.schemas.schemasCongratulation import CreateCongratulation, ShowCongratulation, ShowListCongratulation, UpdatedCongratulationResponse

async def _create_new_congratulation(body: CreateCongratulation, sender_id: UUID, session: AsyncSession) -> ShowCongratulation:
    async with session.begin():
        congratulation_dal = CongratulationDAL(session)
        congratulation, sender, receiver = await congratulation_dal.create_congratulation(
            sender_id=sender_id,
            receiver_id=body.receiver_id,
            message=body.message,
        )

        sender_name = sender.fullname
        receiver_name = receiver.fullname

        return ShowCongratulation(
            id=congratulation.id,
            sender_name=sender_name,
            receiver_name=receiver_name,
            timestamp=congratulation.timestamp,
            message=congratulation.message,
            is_read=congratulation.is_read,
        )
async def _get_congratulation_by_id(congratulation_id: UUID, session: AsyncSession) -> ShowCongratulation:
    async with session.begin():
        congratulation_dal = CongratulationDAL(session)
        congratulation = await congratulation_dal.get_congratulation_by_id(
            congratulation_id=congratulation_id,
        )
        return ShowCongratulation(
            id=congratulation.id,
            sender_name=congratulation.sender.fullname,
            receiver_name=congratulation.receiver.fullname,
            timestamp=congratulation.timestamp,
            message=congratulation.message,
            is_read=congratulation.is_read,
        )

async def _update_congratulation(congratulation_id: UUID, session: AsyncSession) -> UpdatedCongratulationResponse:
    async with session.begin():
        congratulation_dal = CongratulationDAL(session)
        congratulation = await congratulation_dal.update_congratulation(
            congratulation_id=congratulation_id,
        )
        return UpdatedCongratulationResponse(
            id=congratulation.id,
            sender_name=congratulation.sender.fullname,
            receiver_name=congratulation.receiver.fullname,
            timestamp=congratulation.timestamp,
            message=congratulation.message,
            is_read=congratulation.is_read,
        )

async def _get_all_congratulation_is_sender(user_id: UUID, session: AsyncSession) -> List[ShowListCongratulation]:
    async with session.begin():
        congratulation_dal = CongratulationDAL(session)
        all_congratulation_is_sender = await congratulation_dal.get_all_congratulation_is_sender(
            user_id=user_id,
        )
        result = []
        for congratulation in all_congratulation_is_sender:
            result.append(ShowListCongratulation(
                id=congratulation.id,
                sender_name=congratulation.sender.fullname,
                receiver_name=congratulation.receiver.fullname,
                timestamp=congratulation.timestamp,
                is_read=congratulation.is_read,
            ))
        return result


async def _get_all_congratulation_is_followed(user_id: UUID, session: AsyncSession) -> List[ShowListCongratulation]:
    async with session.begin():
        congratulation_dal = CongratulationDAL(session)
        all_congratulation_is_sender = await congratulation_dal.get_all_congratulation_is_followed(
            user_id=user_id,
        )
        result = []
        for congratulation in all_congratulation_is_sender:
            result.append(ShowListCongratulation(
                id=congratulation.id,
                sender_name=congratulation.sender.fullname,
                receiver_name=congratulation.receiver.fullname,
                timestamp=congratulation.timestamp,
                is_read=congratulation.is_read,
            ))
        return result