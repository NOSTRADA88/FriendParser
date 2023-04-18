from aiogram import Dispatcher, Bot, types
from config_data.config import Config, load_config
from config_data.bot_menu import set_main_menu
import asyncio
from handlers import basic_commands_handlers, callback_handlers, fsm_handlers
from aiogram.fsm.storage.memory import MemoryStorage


async def main():

    """ creating bot, dispatcher, storage objects, config """

    config: Config = load_config()
    storage: MemoryStorage = MemoryStorage()

    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher(storage=storage)

    """" including routers """

    dp.include_router(basic_commands_handlers.router)
    dp.include_router(callback_handlers.router)
    dp.include_router(fsm_handlers.router)

    """ skipping all updates, setting menu buttons and starting polling"""

    await bot.delete_webhook(drop_pending_updates=True)
    dp.startup.register(set_main_menu)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

