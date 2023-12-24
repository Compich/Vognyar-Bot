from aiogram.filters.callback_data import CallbackData


class ShowSettings(CallbackData, prefix='ShowSettings'):
    ...


class ChangeMinScoville(CallbackData, prefix='ChangeMinScoville'):
    ...


class SwitchSubscription(CallbackData, prefix='SwitchSubscription'):
    ...
