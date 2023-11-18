from .bot_config import config

if config.emoji:
    DOLLAR = ' 💵 '
    DOOR = ' 🚪 '
    BELL = ' 🔔 '
    CLOCK = ' 🕓 '
    CALENDAR = ' 📅 '
    UNSUBSCRIBE = ' 🔕 '
    PAPYRUS = ' 📜 '
else:
    DOLLAR = ''
    DOOR = ''
    BELL = ''
    CLOCK = ''
    CALENDAR = ''
    UNSUBSCRIBE = ''
    PAPYRUS = ''
