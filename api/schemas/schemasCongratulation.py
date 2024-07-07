import uuid
import datetime
from pydantic import BaseModel

class TunedModel(BaseModel):
    class Config:
        from_attributes = True

class ShowCongratulation(TunedModel):
    id: uuid.UUID
    sender_name: str
    receiver_name: str
    timestamp: datetime.datetime
    message: str
    is_read: bool

class ShowListCongratulation(TunedModel):
    id: uuid.UUID
    sender_name: str
    receiver_name: str
    timestamp: datetime.datetime
    is_read: bool

class UpdatedCongratulationResponse(BaseModel):
    id: uuid.UUID
    sender_name: str
    receiver_name: str
    timestamp: datetime.datetime
    message: str
    is_read: bool

class UpdateCongratulationRequest(BaseModel):
    congratulation_id: uuid.UUID

class CreateCongratulation(TunedModel):
    receiver_id: uuid.UUID
    message: str