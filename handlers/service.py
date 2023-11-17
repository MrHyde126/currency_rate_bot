import logging
from datetime import datetime

import requests
from aiogram.utils.markdown import hbold

from db.functions import save_currency_rate_history


async def get_currency_rate(tg_id: str, date: datetime) -> str:
    """Получает курс доллара."""
    try:
        data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
        formatted_date = date.strftime('%d.%m.%Y %H:%M:%S')
        rate = data['Valute']['USD']['Value']
        await save_currency_rate_history(tg_id, date, rate)
        text = f'Курс доллара на {formatted_date}:\n{hbold(rate)} рублей.'
    except Exception as e:
        logging.exception(e)
        text = 'Произошла ошибка при получении курса.\nПовторите попытку позже.'
    return text
