import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Date
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fullname = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    date_of_birthday = Column(Date, nullable=False)
    is_active = Column(Boolean(), default=True)
    days_before_birthday_alert = Column(Integer, nullable=False, default=3)

    user_jwttoken = relationship("JwtToken", back_populates="jwttoken_user")

    user_sender = relationship("Congratulation", foreign_keys="[Congratulation.sender_id]")
    user_receiver = relationship("Congratulation", foreign_keys="[Congratulation.receiver_id]")

    followers = relationship(
        "User",
        secondary="follows",
        primaryjoin="User.id==Follow.followed_id",
        secondaryjoin="User.id==Follow.follower_id",
        backref="following"
    )


class Follow(Base):
    __tablename__ = "follows"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    follower_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    followed_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)

class Congratulation(Base):
    __tablename__ = "congratulations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sender_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    receiver_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean(), default=False)

    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    followed_user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    alert_date = Column(Date, nullable=False)
    days_before_birthday = Column(Integer, nullable=False)

    user = relationship("User", foreign_keys=[user_id])
    followed_user = relationship("User", foreign_keys=[followed_user_id])

class JwtToken(Base):
    __tablename__ = "jwt_tokens"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("users.id"))
    client_id = Column(String)
    jwt = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    date_of_creation = Column(DateTime(timezone=True), default=datetime.utcnow)

    jwttoken_user = relationship("User", back_populates="user_jwttoken", foreign_keys=[user_id])