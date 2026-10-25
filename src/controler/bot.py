from aiogram import Router, exceptions, Bot
from aiogram.types import Message
from aiogram.filters import Command

from config import logging, StandartLoader
from src.service.service import Service

service = Service()
standart_obj = StandartLoader()

logger = logging.gelLogger(__name__)

router = Router()

@router.message()
async def handler_follow_message(message: Message) -> None:
    await service.update_user_message(user=message.from_user)


async def sender_message(bot: Bot) -> None:
    ready_text = await service.get_all_message_from_data()
    await bot.send_message(
        chat_id=standart_obj.get_output,
        text=ready_text,
        parse_mode="HTML",
    )