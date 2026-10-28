from datetime import datetime
from sqlalchemy import select, desc, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from src.core.database import get_db
from src.models.models import MessageActivity, Followers
from config import logging

logger = logging.getLogger(__name__)


class Repository:
    
    async def update_message_user(self, user_id: int, username: str | None) -> None:
        
        stmt = insert(MessageActivity).values(
            user_id=str(user_id),
            username=username,
            counter_message=1, 
        )
        
        stmt = stmt.on_conflict_do_update(
        index_elements=[MessageActivity.user_id],
        set_={
            "counter_message": MessageActivity.counter_message + 1,
            "username": func.coalesce(stmt.excluded.username, MessageActivity.username),
        },
    )
        
        async with get_db() as db:
    
            try:
                await db.execute(stmt)
                await db.commit()
                       
            except IntegrityError as e:
                await db.rollback()
                logger.warning(
                    "update_message_user: database error | %s (%s)",
                    type(e).__name__,
                    e,
                )
    
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
    
    async def add_new_follower(self, user_id: int, is_premium: bool = False) -> None:
        
        async with get_db() as db:
            try:
                is_exsist = await self._check_exsist_follower(db=db, user_id=user_id)
                
                if is_exsist is None:
                    user = Followers(
                        is_premium=is_premium,
                        user_id=str(user_id),
                    )
                    
                    db.add(user)
                    await db.commit()
                    
                    return None
                    
            except IntegrityError as e:
                logger.warning(
                    "add_new_followers: database error %s (%s)",
                    type(e).__name__,
                    e,
                )
                return None
    
    
    async def _check_exsist_follower(self, *, db: AsyncSession, user_id: int) -> Followers | None:
        try:
            result = await db.execute(select(Followers).where(
                Followers.user_id == str(user_id),
            ))
                
            is_exsist = result.scalar_one_or_none()
                
            return is_exsist
            
        except SQLAlchemyError as e:
            logger.warning(
                "_chech_exsist_follower: database error %s (%s)",
                type(e).__name__,
                e,
            )
            return None
    
    
    async def get_followers(self, data_from: datetime, data_to: datetime) -> list[Followers]:
        
        async with get_db() as db:
            try:
                followers = await db.execute(
                    select(Followers)
                    .where(
                        Followers.created_at >= data_from,
                        Followers.created_at < data_to,
                    )   
                )
                
                return followers.scalars().all()
            
            except SQLAlchemyError as e:
                logger.warning(
                    "get_followers: database error %s (%s)",
                    type(e).__name__,
                    e,
                )
                return []
                            