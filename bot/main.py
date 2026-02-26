import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


from config import settings
from handlers import routers

from database.setup import init_db

async def main() -> None:
    await init_db()
    
    dp = Dispatcher()
     
    for router in routers:
        dp.include_router(router)
        logging.info(f"Connected router: {router}")
    
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
