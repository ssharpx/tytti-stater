from datetime import datetime
from sqlalchemy import DateTime, func, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import BaseModel

class MessageActivity(BaseModel):
    
    __tablename__ = "users_message"
    
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    
    user_id: Mapped[str] = mapped_column(
        String,
        index=True,
        nullable=False,
        unique=True,
    )
    
    username: Mapped[str] = mapped_column(
        String,
        nullable=True,   
    )
    
    counter_message: Mapped[int] = mapped_column(
        server_default="0",
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
    
class Followers(BaseModel):
    
    __tablename__ = "last_followers"
    
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    
    is_premium: Mapped[bool] = mapped_column(
        server_default="false",
    )
    
    user_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
    )