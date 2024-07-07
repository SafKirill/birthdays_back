import uuid
from pydantic import BaseModel


class TunedModel(BaseModel):
    class Config:
        from_attributes = True

class ShowFollow(BaseModel):
    id: uuid.UUID

class CreateFollow(BaseModel):
    followed_id: uuid.UUID