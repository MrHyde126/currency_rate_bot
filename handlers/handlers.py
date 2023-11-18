from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold
from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import callbacks as cb
from config.button_labels import ButtonLabels as bl
from db.functions import (
    create_user_if_not_exists,
    get_currency_rate_history,
    subscription_toggle,
    user_is_subscribed,
)
from utils.bot_utils import bot_answer, get_markup, notification

from .service import get_currency_rate

router = Router(name=__name__)

scheduler = AsyncIOScheduler()


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
    tg_id = str(obj.from_user.id)
    reply_markup = get_markup(
        [(bl.DOLLAR_RATE, cb.DOLLAR_RATE)],
        [
            (bl.SUBSCRIBE, cb.SUBSCRIBE)
            if not await user_is_subscribed(tg_id)
            else (bl.UNSUBSCRIBE, cb.UNSUBSCRIBE)
        ],
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
    tg_id = str(callback.from_user.id)
    text = await get_currency_rate(tg_id)
    reply_markup = get_markup([(bl.MAIN_MENU, cb.MAIN_MENU)])
    await bot_answer(callback, text, reply_markup)


@router.callback_query(F.data.startswith(cb.SUBSCRIBE))
async def subscribe_menu(callback: CallbackQuery) -> None:
    """Позволяет подписаться или отписаться от получения уведомлений о курсе."""
    text = 'Выберите желаемую частоту уведомлений:'
    reply_markup = get_markup(
        [(bl.HOURLY, cb.HOURLY), (bl.DAILY, cb.DAILY)],
        [(bl.MAIN_MENU, cb.MAIN_MENU)],
    )
    await bot_answer(callback, text, reply_markup)


@router.callback_query(F.data.startswith(cb.HOURLY))
async def subscribe_hourly(callback: CallbackQuery, bot: Bot) -> None:
    """Подписка на ежечасное получение уведомлений о курсе."""
    tg_id = str(callback.from_user.id)
    await subscription_toggle(tg_id)
    text = 'Вы подписаны на ежечасное получение уведомлений о курсе.'
    scheduler.add_job(
        notification, 'interval', hours=1, args=[bot, tg_id], id=tg_id
    )
    if not scheduler.running:
        scheduler.start()
    reply_markup = get_markup([(bl.MAIN_MENU, cb.MAIN_MENU)])
    await bot_answer(callback, text, reply_markup)


@router.callback_query(F.data.startswith(cb.DAILY))
async def subscribe_daily(callback: CallbackQuery, bot: Bot) -> None:
    """Подписка на ежедневное получение уведомлений о курсе."""
    tg_id = str(callback.from_user.id)
    await subscription_toggle(tg_id)
    text = 'Вы подписаны на ежедневное получение уведомлений о курсе.'
    scheduler.add_job(
        notification, 'interval', days=1, args=[bot, tg_id], id=tg_id
    )
    if not scheduler.running:
        scheduler.start()
    reply_markup = get_markup([(bl.MAIN_MENU, cb.MAIN_MENU)])
    await bot_answer(callback, text, reply_markup)


@router.callback_query(F.data.startswith(cb.UNSUBSCRIBE))
async def unsubscribe(callback: CallbackQuery) -> None:
    """Отписка от получения уведомлений о курсе."""
    tg_id = str(callback.from_user.id)
    await subscription_toggle(tg_id)
    try:
        scheduler.remove_job(tg_id)
    except JobLookupError:
        pass
    text = 'Вы отписаны от получения уведомлений о курсе.'
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
