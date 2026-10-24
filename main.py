import asyncio
from aiogram import Bot, Dispatcher
from config import logging, StandartLoader

logger = logging.getLogger()
loader_obj = StandartLoader()


async def main() -> None:
    
    logger.info(
        "program installation process..."
    )
    
    bot = Bot(token=loader_obj.get_token_bot)
    dp = Dispatcher()
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())