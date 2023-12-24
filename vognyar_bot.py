import tasks


import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types.bot_command import BotCommand
from aiogram.types.bot_command_scope_default import BotCommandScopeDefault
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import config
import handlers
import middlewares as mdlw


async def setup_scheduler(bot: Bot, timezone: str = 'Europe/Kiev'):
    timezone = 'Europe/Kiev'
    scheduler = AsyncIOScheduler(timezone=timezone)
    scheduler.add_job(
        func=tasks.check_sauces,
        trigger='cron',
        second=0,
        kwargs={
            'bot': bot
        }
    )
    scheduler.start()


async def on_startup(bot: Bot):
    default_commands = [
        BotCommand(
            command='settings',
            description='Открыть настройки'
        ),
        BotCommand(
            command='subscribe',
            description='Подписаться на уведомления'
        ),
        BotCommand(
            command='unsubscribe',
            description='Отписаться от уведомлений'
        )
    ]

    await bot.set_my_commands(
        commands=default_commands,
        scope=BotCommandScopeDefault()
    )

    await setup_scheduler(bot=bot)


async def main():
    dispatcher = Dispatcher()
    bot = Bot(config.BOT_TOKEN, parse_mode='MarkdownV2')

    dispatcher.include_routers(
        handlers.user_router
    )

    dispatcher.startup.register(on_startup)

    dispatcher.message.middleware(mdlw.UpdateUserMiddleware())
    dispatcher.callback_query.middleware(mdlw.UpdateUserMiddleware())

    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.WARNING,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.warning('Vognyar Bot')

    asyncio.run(main())
