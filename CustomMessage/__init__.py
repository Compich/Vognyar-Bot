from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class CustomMessage(object):
    """Класс для создания сообщений для телеграма с текстом и клавиатурой."""

    def __init__(
        self,
        text='',
        keyboard: list=None
    ):
        """
        Конструктор класса CustomMessage.

        Args:
            text: Текст сообщения
            keyboard: Клавиатура сообщения
        """
        self._text = text
        if keyboard is not None:
            self._keyboard = keyboard
        else:
            self._keyboard = []

    def add_text(self, text: str, sep='\n') -> None:
        """
        Добавляет текст к уже созданному сообщению.

        Args:
            text: Текст, который требуется добавить к уже существующему тексту
            sep: Разделитель между строками, которые добавляются
        """
        self._text += sep + text

    def set_text(self, to_set: str) -> None:
        """
        Полностью заменяет текст уже созданного сообщения.

        Args:
            to_set: Текст, который нужно установить
        """
        self._text = to_set

    def add_rows(self, *args) -> None:
        """
        Добавляет строчки к клавиатуре.

        Args:
            args: Строки, которые нужно добавить
        """
        for row in args:
            if isinstance(row, InlineKeyboardButton):
                row = [row]
            self._keyboard.append(row)


    @property
    def text(self) -> str:
        """
        Возвращает текст сообщения.

        Returns:
            self.message_text (str): Текст сообщения
        """
        return self._text

    @property
    def keyboard(self) -> InlineKeyboardMarkup:
        """
        Возвращает клавиатуру сообщения.

        Returns:
            self.message_reply_markup (InlineKeyboardMarkup): Клавиатура
            сообщения
        """
        return InlineKeyboardMarkup(
            inline_keyboard=self._keyboard
        )


    def unpack(self):
        return {
            'text': self.text,
            'reply_markup': self.keyboard
        }
