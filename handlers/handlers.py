from datetime import datetime

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold

from config import callbacks as cb
from config.button_labels import ButtonLabels as bl
from db.functions import create_user_if_not_exists, get_currency_rate_history
from utils.bot_utils import bot_answer, get_markup

from .service import get_currency_rate

router = Router(name=__name__)


async def main_menu_generic(
    obj: Message | CallbackQuery,
    greetings: bool = False,
) -> None:
    """Генерирует главное меню."""
    MAIN_MENU_TITLE = 'Главное меню'
    text = (
        f'Добро пожаловать, {obj.from_user.full_name}!\n\n{MAIN_MENU_TITLE}'
        if greetings
        else MAIN_MENU_TITLE
    )
    reply_markup = get_markup(
        [(bl.DOLLAR_RATE, cb.DOLLAR_RATE)],
        [(bl.SUBSCRIBE, cb.SUBSCRIBE)],
        [(bl.HISTORY, cb.HISTORY)],
    )
    await bot_answer(obj, text, reply_markup)


@router.message(CommandStart())
async def start(message: Message) -> None:
    """Отображает главное меню с приветствием."""
    await create_user_if_not_exists(message)
    await main_menu_generic(message, greetings=True)


@router.callback_query(F.data.startswith(cb.MAIN_MENU))
async def main_menu(callback: CallbackQuery) -> None:
    """Отображает главное меню без приветствия."""
    await main_menu_generic(callback)


@router.callback_query(F.data.startswith(cb.DOLLAR_RATE))
async def dollar_rate(callback: CallbackQuery) -> None:
    """Отображает курс доллара."""
    date = datetime.now()
    tg_id = str(callback.from_user.id)
    text = await get_currency_rate(tg_id, date)
    reply_markup = get_markup([(bl.MAIN_MENU, cb.MAIN_MENU)])
    await bot_answer(callback, text, reply_markup)


@router.callback_query(F.data.startswith(cb.SUBSCRIBE))
async def subscribe(callback: CallbackQuery) -> None:
    """Позволяет подписаться или отписаться от получения уведомлений о курсе."""
    text = 'Подписка на уведомления о курсе.'
    reply_markup = get_markup([(bl.MAIN_MENU, cb.MAIN_MENU)])
    await bot_answer(callback, text, reply_markup)


@router.callback_query(F.data.startswith(cb.HISTORY))
async def history(callback: CallbackQuery) -> None:
    """Отображает историю получения курса."""
    text = 'История получения курса доллара:\n\n'
    tg_id = str(callback.from_user.id)
    history = await get_currency_rate_history(tg_id)
    for item in history:
        formatted_date = item.date.strftime('%d.%m.%Y %H:%M:%S')
        text += f'{formatted_date} - {hbold(item.rate)} р.\n'
    reply_markup = get_markup([(bl.MAIN_MENU, cb.MAIN_MENU)])
    await bot_answer(callback, text, reply_markup)
