from datetime import datetime

from aiogram.types import Message
from sqlalchemy import select

from .models import CurrencyRateHistory, User
from .utils import DATABASE_URL, get_db_session


async def create_user_if_not_exists(message: Message) -> None:
    """Создает нового пользователя, если пользователь с таким telegram_id не существует."""
    async with await get_db_session(DATABASE_URL) as session:
        async with session.begin():
            tg_id = str(message.from_user.id)
            query = select(User).where(User.telegram_id == tg_id)
            user = await session.scalar(query)

            if not user:
                user = User(
                    name=message.from_user.full_name,
                    telegram_id=tg_id,
                )
                session.add(user)
                await session.commit()


async def save_currency_rate_history(
    tg_id: str, date: datetime, rate: float
) -> None:
    """Сохраняет запрос в историю курса валют."""
    async with await get_db_session(DATABASE_URL) as session:
        async with session.begin():
            query = select(User).where(User.telegram_id == tg_id)
            user = await session.scalar(query)
            if not user:
                return

            currency_rate_history = CurrencyRateHistory(
                user_id=user.id, date=date, rate=rate
            )
            session.add(currency_rate_history)
            await session.commit()


async def get_currency_rate_history(tg_id: str) -> list[CurrencyRateHistory]:
    """Получает историю запросов курса валют определенного пользователя."""
    async with await get_db_session(DATABASE_URL) as session:
        async with session.begin():
            user_query = select(User).where(User.telegram_id == tg_id)
            user = await session.scalar(user_query)
            if not user:
                return []

            history_query = (
                select(CurrencyRateHistory)
                .where(CurrencyRateHistory.user_id == user.id)
                .limit(20)
                .order_by(CurrencyRateHistory.date.desc())
            )
            return await session.scalars(history_query)


async def subscription_toggle(tg_id: str) -> None:
    """Переключает состояние подписки пользователя."""
    async with await get_db_session(DATABASE_URL) as session:
        async with session.begin():
            user_query = select(User).where(User.telegram_id == tg_id)
            user = await session.scalar(user_query)
            if not user:
                return False

            user.subscribed = not user.subscribed
            await session.commit()


async def user_is_subscribed(tg_id: str) -> bool:
    """Проверяет подписан ли пользователь."""
    async with await get_db_session(DATABASE_URL) as session:
        async with session.begin():
            user_query = select(User).where(User.telegram_id == tg_id)
            user = await session.scalar(user_query)
            if not user:
                return False
            return user.subscribed
