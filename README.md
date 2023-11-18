# Currency Rate Bot

Телеграм бот для получения информации о курсе доллара и уведомлений.

### Инструкция по запуску:

1. Клонировать репозиторий `git clone git@github.com:MrHyde126/currency_rate_bot.git`
2. Создать файл .env `cp .env_example .env` и отредактировать его
3. Установить Pipenv:
   - MacOS: `brew install pipenv`
   - Linux: `sudo pip install pipenv`
   - Windows: `pip install pipenv`
4. Активировать виртуальное окружение `pipenv shell --python 3.11`
5. Установить все зависимости `pipenv install`
6. Установить [Docker](https://www.docker.com/products/docker-desktop/) и запустить его
7. Выполнить в терминале команду `docker compose up -d`
8. Запустить бота `pipenv run python main.py`
9. Если вы использовали указанный токен для другого бота, то понадобится повторно ввести команду `/start`
