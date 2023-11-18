from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    Message,
    TelegramObject,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from handlers.service import get_currency_rate


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


async def notification(
    bot: Bot, tg_id: str, parse_mode: str = ParseMode.HTML
) -> Message:
    """Отправляет уведомление о курсе в чат."""
    text = await get_currency_rate(tg_id)
    return await bot.send_message(tg_id, text, parse_mode=parse_mode)
