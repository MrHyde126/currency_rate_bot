import asyncio
import logging

from aiogram import Bot, Dispatcher

from config.bot_config import config
from handlers import main_menu


async def start() -> None:
    """Точка входа. Запускает бота."""
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    dp.include_routers(
        main_menu.router,
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start())
