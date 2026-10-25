from sqlalchemy import select
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
            
            