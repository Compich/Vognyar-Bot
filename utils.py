import logging

from aiogram import Bot

import message_generators as msggen
from database import models as dbm


async def send_new_sauce(bot: Bot, sauce: dbm.Sauce):
    message = msggen.get_new_sauce_message(sauce=sauce)
    users = dbm.User.get_all(
        dbm.User.subscribed &
        (dbm.User.min_scoville_heat_units <= sauce.scoville_heat_units)
    )

    for user in users:
        try:
            if sauce.img_url:
                await bot.send_photo(
                    chat_id=user.user_id,
                    photo=sauce.img_url,
                    caption=message.text,
                    reply_markup=message.keyboard
                )
            else:
                await bot.send_message(
                    chat_id=user.user_id,
                    text=message.text,
                    reply_markup=message.keyboard
                )
        except Exception as e:
            logging.error(f'Error sending message to user {user.user_id}: {e}')


async def send_stock_status_change(bot: Bot, sauce: dbm.Sauce):
    message = msggen.get_stock_status_change_message(sauce=sauce)
    users = dbm.User.get_all(
        dbm.User.subscribed &
        (dbm.User.min_scoville_heat_units <= sauce.scoville_heat_units)
    )

    for user in users:
        try:
            if sauce.img_url:
                await bot.send_photo(
                    chat_id=user.user_id,
                    photo=sauce.img_url,
                    caption=message.text,
                    reply_markup=message.keyboard
                )
            else:
                await bot.send_message(
                    chat_id=user.user_id,
                    text=message.text,
                    reply_markup=message.keyboard
                )
        except Exception as e:
            logging.error(f'Error sending message to user {user.user_id}: {e}')
