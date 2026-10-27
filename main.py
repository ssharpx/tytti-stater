import asyncio
from datetime import timezone
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import logging, StandartLoader, UPDATE_TIME
from src.controler.bot import router, sender_message
from src.core.database import BaseModel, engine as message_table

logger = logging.getLogger()
scheduler = AsyncIOScheduler(timezone=timezone.utc)

loader_obj = StandartLoader()

bot = Bot(token=loader_obj.get_token_bot)

async def schedule_sender() -> None:
    
    logger.info(
        "schedule_sender: process started..."
    )
    
    await sender_message(bot=bot)

async def main() -> None:
    
    logger.info(
        "program installation process..."
    )
    
    dp = Dispatcher()
    
    await create_table()
    
    scheduler.add_job(
        schedule_sender,
        "cron",
        hour=19,
        minute=13,
        misfire_grace_time=300,
        timezone=timezone.utc,
        max_instances=1,
        coalesce=True,
    )
    
    scheduler.start()
    
    try:
        
        logger.info(
            "the process has been successfully started"
        )
        dp.include_router(router)
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
        )   
        
    finally:
        
        logger.info(
            "the process stopped working"
        )
        
        scheduler.shutdown(wait=False)
        await message_table.dispose()
        await bot.session.close()


async def create_table() -> None:
    async with message_table.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(main())