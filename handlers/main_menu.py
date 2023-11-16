from datetime import datetime

import requests
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold

from config import callbacks as cb
from config.button_labels import ButtonLabels as bl
from utils.bot_utils import bot_answer, get_markup

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
    reply_markup = get_markup([(bl.DOLLAR_RATE, cb.DOLLAR_RATE)])
    await bot_answer(obj, text, reply_markup)


@router.message(CommandStart())
async def start(message: Message) -> None:
    """Отображает главное меню с приветствием."""
    await main_menu_generic(message, greetings=True)


@router.callback_query(F.data.startswith(cb.MAIN_MENU))
async def main_menu(callback: CallbackQuery) -> None:
    """Отображает главное меню без приветствия."""
    await main_menu_generic(callback)


@router.callback_query(F.data.startswith(cb.DOLLAR_RATE))
async def dollar_rate(callback: CallbackQuery) -> None:
    """Отображает курс доллара."""
    try:
        data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
        date = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        rate = hbold(data['Valute']['USD']['Value'])
        text = f'Курс доллара на {date}:\n{rate} рублей.'
    except Exception:
        text = 'Произошла ошибка при получении курса.\nПовторите попытку позже.'
    reply_markup = get_markup([(bl.BACK, cb.MAIN_MENU)])
    await bot_answer(callback, text, reply_markup)
