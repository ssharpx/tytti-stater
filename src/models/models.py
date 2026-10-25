from datetime import datetime
from sqlalchemy import DateTime, func, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import BaseModel

class AllMessages:
    
    def __init__(self, *, all_message: int, date: datetime):
        self.all_message = all_message
        self.date = date,

class MessageActivity(BaseModel):
    
    __tablename__ = "users_message"
    
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    
    user_id: Mapped[int] = mapped_column(
        index=True,
        nullable=False,
        unique=True,
    )
    
    username: Mapped[str] = mapped_column(
        String,
        nullable=True,   
    )
    
    counter_message: Mapped[int] = mapped_column(
        server_default=0,
    )
    
    last_message: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        index=True,
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    
class LastFollower(BaseModel):
    
    __tablename__ = "last_followers"
    
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    
    is_premium: Mapped[Boolean] = mapped_column(
        server_default=False,
        index=True,
    )
    
    user_id: Mapped[int] = mapped_column(
        nullable=False,
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_defautl=func.now(),
        index=True,
    )