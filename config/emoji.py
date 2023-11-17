from .bot_config import config

if config.emoji:
    DOLLAR = ' 💵 '
    BACK = ' 👈🏼 '
    DOOR = ' 🚪 '
    BELL = ' 🔔 '
    PAPYRUS = ' 📜 '
else:
    DOLLAR = ''
    BACK = ''
    DOOR = ''
    BELL = ''
    PAPYRUS = ''
