from database import models as dbm
from CustomMessage import CustomMessage
import markdown as md
from aiogram import types
import callback_datas as cbds


def get_start_message() -> CustomMessage:
    return CustomMessage(
        text=md.text(
            md.quote(
                'Привет! Я бот для отправки уведомлений о появлении в',
                'наличии соусов или появлении новых на сайте',
                'https://vognyar.com/ru/ekstragostra-serija/',
            ),
            md.text(
                'Чтобы подписаться на уведомления, введите команду',
                md.bold('/subscribe')
            ),
            md.text(
                'Также по команде',
                md.bold('/settings'),
                'Вы можете открыть настройки, в которых настроить, начиная',
                'с какой остроты соусов Вам будут приходить уведомления'
            ),
            sep='\n\n'
        )
    )


def get_sauce_message(sauce: dbm.Sauce) -> CustomMessage:
    return CustomMessage(
        text=md.text(
            md.text('Название:', md.bold(sauce.name)),
            md.text('Острота:', md.bold(sauce.scoville_heat_units), 'SHU'),
            md.text('Цена:', md.bold(sauce.price), md.quote('грн.')),
            md.text('В наличии:', '✅' if sauce.in_stock else '❌'),
            sep='\n'
        ),
        keyboard=[[
            types.InlineKeyboardButton(
                text='🌐 Перейти на страницу соуса',
                url=sauce.link
            )
        ]]
    )


def get_new_sauce_message(sauce: dbm.Sauce) -> CustomMessage:
    sauce_message = get_sauce_message(sauce)

    text = md.text(
        md.quote('🌶 В продаже появился новый соус!'),
        sauce_message.text,
        sep='\n\n'
    )

    sauce_message.set_text(text)
    return sauce_message


def get_stock_status_change_message(sauce: dbm.Sauce) -> CustomMessage:
    sauce_message = get_sauce_message(sauce)

    if sauce.in_stock:
        stock_text = '😋🌶 Соус снова появился в продаже!'
    else:
        stock_text = '😔🌶 Соус закончился!'

    text = md.text(
        md.quote(stock_text),
        sauce_message.text,
        sep='\n\n'
    )

    sauce_message.set_text(text)
    return sauce_message


def get_settings_message(user: dbm.User) -> CustomMessage:
    text = md.text(
        md.text(
            '🌶 Минимальная острота:',
            md.bold(f'{user.min_scoville_heat_units:,} SHU')
        ),
        md.text(
            '🔔 Подписка на уведомления:',
            '✅' if user.subscribed else '❌'
        ),
        sep='\n'
    )

    if user.subscribed:
        subscription_text = 'Отписаться от уведомлений'
    else:
        subscription_text = 'Подписаться на уведомления'

    keyboard = [
        [
            types.InlineKeyboardButton(
                text='🌶 Изменить минимальную остроту',
                callback_data=cbds.ChangeMinScoville().pack()
            )
        ],
        [
            types.InlineKeyboardButton(
                text=f'🔔 {subscription_text}',
                callback_data=cbds.SwitchSubscription().pack()
            )
        ]
    ]

    return CustomMessage(
        text=text,
        keyboard=keyboard
    )


def get_min_scoville_message() -> CustomMessage:
    return CustomMessage(
        text=md.italic(
            '🌶 Введите новое значение минимального количества',
            'Scoville Heat Units (SHU) для получения уведомлений'
        ),
        keyboard=[[
            types.InlineKeyboardButton(
                text='↩️ Вернуться',
                callback_data=cbds.ShowSettings().pack()
            )
        ]]
    )
