import re
import uuid
import datetime
from pydantic import BaseModel
from pydantic import constr


class TunedModel(BaseModel):
    class Config:
        from_attributes = True

class ShowUser(TunedModel):
    id: uuid.UUID
    fullname: str
    date_of_birthday: datetime.date

class CreateUser(TunedModel):
    fullname: str
    password: constr(min_length=6)
    email: str
    date_of_birthday: datetime.date

class UpdatedUserResponse(BaseModel):
    updated_user_id: uuid.UUID

class UpdateUserRequest(BaseModel):
    days_before_birthday_alert: int

class ShowAllUsers(TunedModel):
    id: uuid.UUID
    fullname: str
    date_of_birthday: datetime.date
    signed: bool

class ShowUserInfo(TunedModel):
    days_before_birthday_alert: int