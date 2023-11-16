from aiogram.enums import ParseMode
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    Message,
    TelegramObject,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


def get_markup(*buttons: list[tuple[str, str]]) -> InlineKeyboardMarkup:
    """Генерирует клавиатуру из переданных кнопок."""
    kb_builder = InlineKeyboardBuilder()
    for button in buttons:
        bts = [
            InlineKeyboardButton(text=text, callback_data=callback_data)
            for text, callback_data in button
        ]
        kb_builder.row(*bts)
    return kb_builder.as_markup()


async def bot_answer(
    event: TelegramObject,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
    parse_mode: str = ParseMode.HTML,
) -> Message | None:
    """Отправляет сообщение в чат."""
    kwargs = {'parse_mode': parse_mode, 'reply_markup': reply_markup}
    if isinstance(event, Message):
        return await event.answer(text, **kwargs)
    elif isinstance(event, CallbackQuery):
        await event.message.edit_text(text, **kwargs)
        await event.answer()
