from typing import Any, Sequence

from aiogram import md


def _join(*args: Sequence[Any], sep=' ') -> str:
    return sep.join(map(str, args))


text = _join
custom_emoji = md.custom_emoji


def pre_language(replacement_text: str, language: str) -> str:
    return md.pre_language(value=quote(replacement_text), language=language)


def link(replacement_text: str, link: str) -> str:
    return md.link(value=quote(replacement_text), link=link)


def bold(*args: Sequence[Any], sep=' ') -> str:
    return md.bold(quote(*args, sep=sep))


def italic(*args: Sequence[Any], sep=' ') -> str:
    return md.italic(quote(*args, sep=sep))


def code(*args: Sequence[Any], sep=' ') -> str:
    return md.code(quote(*args, sep=sep))


def pre(*args: Sequence[Any], sep=' ') -> str:
    return md.pre(quote(*args, sep=sep))


def underline(*args: Sequence[Any], sep=' ') -> str:
    return md.underline(quote(*args, sep=sep))


def strikethrough(*args: Sequence[Any], sep=' ') -> str:
    return md.strikethrough(quote(*args, sep=sep))


def spoiler(*args: Sequence[Any], sep=' ') -> str:
    return md.spoiler(quote(*args, sep=sep))


def quote(*args: Sequence[Any], sep=' ') -> str:
    return md.quote(_join(*args, sep=sep))
