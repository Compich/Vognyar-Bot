import re

from aiogram import Router, F
from aiogram import filters, types
from aiogram.fsm.context import FSMContext

import markdown as md
import message_generators as msggen
from database import models as dbm
import callback_datas as cbds
from states import States

user_router = Router()


@user_router.message(
    filters.Command(commands='start')
)
async def start(message: types.Message):
    start_message = msggen.get_start_message()

    await message.answer(
        text=start_message.text,
        disable_web_page_preview=True
    )


@user_router.message(
    filters.Command(commands='subscribe')
)
async def subscribe(message: types.Message, user: dbm.User):
    if user.subscribed:
        await message.answer(
            text=md.italic('Вы уже подписаны на уведомления')
        )
    else:
        user.update(subscribed=True)
        await message.answer(
            text=md.italic('Вы успешно подписались на уведомления')
        )


@user_router.message(
    filters.Command(commands='unsubscribe')
)
async def unsubscribe(message: types.Message, user: dbm.User):
    if user.subscribed:
        user.update(subscribed=False)
        await message.answer(
            text=md.italic('Вы успешно отписались от уведомлений')
        )

    else:
        await message.answer(
            text=md.italic('Вы не подписаны на уведомления')
        )


@user_router.message(
    filters.Command(commands='settings')
)
async def settings(message: types.Message, user: dbm.User):
    settings_message = msggen.get_settings_message(user)

    await message.answer(
        text=settings_message.text,
        reply_markup=settings_message.keyboard,
    )


@user_router.callback_query(
    cbds.ShowSettings.filter()
)
async def show_settings_cb(
    call: types.CallbackQuery,
    state: FSMContext,
    user: dbm.User
):
    await state.clear()

    settings_message = msggen.get_settings_message(user)

    await call.message.edit_text(
        text=settings_message.text,
        reply_markup=settings_message.keyboard,
    )


@user_router.callback_query(
    cbds.ChangeMinScoville.filter()
)
async def change_min_scoville_cb(
    call: types.CallbackQuery,
    state: FSMContext
):
    min_scoville_message = msggen.get_min_scoville_message()

    await call.message.edit_text(
        text=min_scoville_message.text,
        reply_markup=min_scoville_message.keyboard,
    )

    await state.set_state(States.new_min_scoville)

    await state.update_data(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id
    )


@user_router.message(
    F.text,
    filters.StateFilter(States.new_min_scoville)
)
async def new_min_scoville(
    message: types.Message,
    state: FSMContext,
    user: dbm.User
):
    state_data = await state.get_data()
    chat_id = state_data['chat_id']
    message_id = state_data['message_id']

    text = message.text

    if chat_id != message.chat.id:
        return

    if text.isdigit():
        min_scoville = int(text)

        user = user.update(min_scoville_heat_units=min_scoville)

        await message.delete()

        settings_message = msggen.get_settings_message(user)

        await message.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=settings_message.text,
            reply_markup=settings_message.keyboard
        )
    else:
        await message.answer(
            text=md.italic('❗️Введена некорректная острота')
        )


@user_router.callback_query(
    cbds.SwitchSubscription.filter()
)
async def switch_subscription_cb(
    call: types.CallbackQuery,
    user: dbm.User
):
    user = user.update(subscribed=not user.subscribed)

    if user.subscribed:
        await call.answer('Вы успешно подписались на уведомления')
    else:
        await call.answer('Вы успешно отписались от уведомлений')

    settings_message = msggen.get_settings_message(user)

    await call.message.edit_text(
        text=settings_message.text,
        reply_markup=settings_message.keyboard,
    )
