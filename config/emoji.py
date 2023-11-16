from .bot_config import config

if config.emoji:
    DOLLAR = ' 💵 '
    BACK = ' 👈🏼 '
    DOOR = ' 🚪 '
else:
    DOLLAR = ''
    BACK = ''
    DOOR = ''
