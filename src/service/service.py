from datetime import datetime, timezone, timedelta
from aiogram.types import User

from src.repository.repository import Repository
from config import logging

logger = logging.getLogger(__name__)

repo = Repository()


class Service:

    async def update_user_message(self, user: User) -> None:
        await repo.update_message_user(user_id=user.id, username=user.username)
    
    async def add_new_chat_member(self, user: User) -> None:
            await repo.add_new_follower(user_id=user.id, is_premium=user.is_premium)
    
    async def clear_table_message(self) -> None:
        await repo.clear_table_message()
        
    
    async def get_all_message_from_data(self) -> str:
        
        data_from = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        data_to = data_from + timedelta(days=1)
        
        result_obj = await repo.get_all_message_data()
        top_users_obj = await repo.get_top_users()
        followers_obj = await repo.get_followers(data_from=data_from, data_to=data_to)
        
        if not result_obj:
            return "No data available for statistics"
        
        all_message = sum(m.counter_message for m in result_obj if m.counter_message > 0)
        all_followers = sum(1 for user in followers_obj)
        all_premium = sum(1 for m in followers_obj if m.is_premium)
        
        users: list[tuple[str, int]] = [
            (f"{u.username}" if u.username else "No username user", u.counter_message)
            for u in top_users_obj or []
        ]
        
        await self.clear_table_message()
        
        return self._get_text_for_statistic(
            date=data_from.strftime("%d.%m.%Y"),
            all_message_count=all_message,
            users=users,
        )

    
    def _get_text_for_statistic(
        self, *, 
        date: str, 
        all_message_count, 
        users: list[tuple[str, int]],
        new_followers: int,
        count_premium: int,
    ) -> str:
        
        top_users = "\n".join(f"{i}. {username} ({count_message})" for i, username, count_message in enumerate(users, start=1)) or "-"
            
        return (
            f"<b>Your chat statistics for {date}:</b>\n\n"
            f"➕ New followers: +{new_followers}\n"
            f"🟩 Premium accounts among new subscribers: {count_premium}\n\n"
            f"✍️ Total messages sent: {all_message_count}\n\n"
            f"👥 Top users: {top_users}"
            )
