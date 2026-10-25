import asyncio
from aiogram import Bot, Dispatcher

from config import logging, StandartLoader
from src.core.database import BaseModel, engine as message_table
logger = logging.getLogger()
loader_obj = StandartLoader()


async def main() -> None:
    
    logger.info(
        "program installation process..."
    )
    
    bot = Bot(token=loader_obj.get_token_bot)
    dp = Dispatcher()
    
    await create_table()
    
    try:
        
        logger.info(
            "the process has been successfully started"
        )
        
        await dp.start_polling(bot)
        
    finally:
        
        logger.info(
            "the process stopped working"
        )
        
        await bot.session.close()


async def create_table() -> None:
    async with message_table.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(main())