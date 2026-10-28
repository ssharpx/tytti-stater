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
            await repo.add_new_follower(user_id=user.id, is_premium=bool(user.is_premium))
    
    async def clear_table_message(self) -> None:
        await repo.clear_table_message()
        
    
    async def get_all_message_from_data(self) -> str:
        
        data_to = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        data_from = data_to - timedelta(days=1)
        
        result_obj = await repo.get_all_message_data()
        top_users_obj = await repo.get_top_users()
        followers_obj = await repo.get_followers(data_from=data_from, data_to=data_to)
        
        all_message = sum(m.counter_message for m in result_obj or [])
        all_followers = len(followers_obj)
        all_premium = sum(1 for m in followers_obj if m.is_premium)
        
        users: list[tuple[str, int]] = [
            (f"{u.username}" if u.username else "No username user", u.counter_message)
            for u in top_users_obj or []
        ]
        
        return self._get_text_for_statistic(
            date=data_from.strftime("%d.%m.%Y"),
            all_message_count=all_message,
            users=users,
            new_followers=all_followers,
            count_premium=all_premium
        )

    
    def _get_text_for_statistic(
        self, *, 
        date: str, 
        all_message_count, 
        users: list[tuple[str, int]],
        new_followers: int,
        count_premium: int,
    ) -> str:
        
        top_users = "\n".join(f"{i}. {username} ({count_message})" for i, (username, count_message) in enumerate(users, start=1)) or "-"
            
        return (
                f"<b>Chat statistics for {date}:</b>\n\n"
                f"➕ New followers: <b>+{new_followers}</b>\n"
                f"🟩 Premium accounts among new subscribers: <b>{count_premium}</b>\n\n"
                f"✍️ <b>Total messages sent: {all_message_count}</b>\n\n"
                f"👥 Top users: \n{top_users}"
            )
