from aiogram import Router, exceptions, Bot
from aiogram.types import Message, ChatMemberUpdated
from aiogram.filters import Command, ChatMemberUpdatedFilter, JOIN_TRANSITION

from config import logging, StandartLoader
from src.service.service import Service

service = Service()
standart_obj = StandartLoader()

logger = logging.getLogger(__name__)

router = Router()

@router.message()
async def handler_follow_message(message: Message) -> None:
    await service.update_user_message(user=message.from_user)

@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def event_join_new_chat_member(event: ChatMemberUpdated):
    await service.add_new_chat_member(user=event.from_user)


async def sender_message(bot: Bot) -> None:
    ready_text = await service.get_all_message_from_data()
    
    await bot.send_message(
        chat_id=standart_obj.get_output,
        text=ready_text,
        parse_mode="HTML",
    )
    
    await service.clear_table_message()