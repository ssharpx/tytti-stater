from datetime import datetime
from sqlalchemy import select, desc, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from src.core.database import get_db
from src.models.models import MessageActivity
from config import logging

logger = logging.getLogger(__name__)


class Repository:
    
    async def update_message_user(self, user_id: int, username: str | None) -> None:
        
        async with get_db() as db:
    
            try:
                user = await self._get_user_exsist(
                    db=db,
                    user_id=user_id,
                )
                
                if user:
                    user.counter_message += 1
                    db.add(user)
                
                else:
                    new_user = MessageActivity(
                        user_id=user_id,
                        username=username,
                    )
                    
                    db.add(new_user)
                
                await db.commit()
                return None
                    
            except IntegrityError as e:
                await db.rollback()
                logger.warning(
                    "update_message_user: database error | %s (%s)",
                    type(e).__name__,
                    e,
                )
                return None
    
    
    async def _get_user_exsist(self, *, db: AsyncSession, user_id: int) -> MessageActivity | None:
        
        try:
            
            result = await db.execute(
                select(MessageActivity).where(
                    MessageActivity.user_id == user_id,
                )
            )
            
            return result.scalar_one_or_none()
        
        except SQLAlchemyError as e:
            logger.warning(
                "_get_user_exsist: database error | %s (%s)",
                type(e).__name__,
                e,
            )
            return None
    
    
    async def clear_table_message(self) -> None:
        
        async with get_db() as db:
            
            try:
                await db.execute(delete(MessageActivity))
                await db.commit()
                
                logger.info(
                    "clear_table_message: tables successfully cleared"
                )
                return None
            
            except SQLAlchemyError as e:        
                logger.warning(
                    "clear_table_message: failed to clear the tables: %s (%s)",
                    type(e).__name__,
                    e,
                )
                return None
        
    
    async def get_all_message_data(self) -> list[MessageActivity] | None:
        
        async with get_db() as db:
            try:
                result_obj = await db.execute(
                    select(MessageActivity)
                )
                
                return result_obj.scalars().all()

            except SQLAlchemyError as e:
                logger.warning(
                    "get_all_message_data: database error: %s (%s)",
                    type(e).__name__,
                    e,
                )
                return None
            
    async def get_top_users(self) -> list[MessageActivity] | None:
        
        async with get_db() as db:
            
            try:
                result_obj = await db.execute(
                    select(MessageActivity)
                    .order_by(
                        desc(MessageActivity.counter_message)
                    ).limit(10)
                )
                
                return result_obj.scalars().all()
            
            except SQLAlchemyError as e:
                logger.warning(
                    "get_top_users: database error: %s (%s)",
                    type(e).__name__,
                    e,
                )
                return None
                
                            