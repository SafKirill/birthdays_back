import uuid
import datetime

from pydantic import BaseModel

class TunedModel(BaseModel):
    class Config:
        from_attributes = True

class ShowJwtService(TunedModel):
    email: str
    id: str
    jwt: str

class ShowJwtToken(TunedModel):
    user_id: uuid.UUID
    jwt: str
    client_id: str = None
    date_of_creation: datetime.datetime
    is_active: bool

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: uuid.UUID
    full_name: str

class JwtTokenCreate(BaseModel):
    user_id: uuid.UUID
    jwt: str
    client_id: str = None
    date_of_creation: datetime.datetime = datetime.datetime.utcnow()

class DeleteJwtTokenResponse(BaseModel):
    deleted_jwt_token_id: uuid.UUID
    client_id: str

class Logout(BaseModel):
    logout_user: bool