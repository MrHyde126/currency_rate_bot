from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    """Базовая модель, определяющая названия таблиц и id."""

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    """Модель пользователя."""

    name: Mapped[str | None]
    telegram_id: Mapped[str] = mapped_column(unique=True, index=True)
    subscribed: Mapped[bool] = mapped_column(default=False)
    currency_rate_history: Mapped['CurrencyRateHistory'] = relationship()


class CurrencyRateHistory(Base):
    """Модель истории курса валют."""

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    date: Mapped[datetime]
    rate: Mapped[float]
