from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/start', description='Начало работы с ботом'),
        BotCommand(command='/stop', description='Нужно нажать после внесения данных о клиенте'),
        BotCommand(command='/add', description='Добавить нового менеджера'),
        BotCommand(command='/remove', description='Удалить менеджера'),
    ]
    await bot.set_my_commands(main_menu_commands)
