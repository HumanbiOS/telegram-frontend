import os
from dotenv import load_dotenv
load_dotenv()
# Telegram token
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
# Security tokens
SERVER_TOKEN = os.getenv("SERVER_TOKEN", "")
# Sever url
SERVER_URL = os.getenv("SERVER_URL", "")
# instance url
INSTANCE_URL = os.getenv("INSTANCE_URL")
# telegram channels if existing
TELEGRAM_DOCTOR_ROOM = os.getenv("TELEGRAM_DOCTOR_ROOM", None)
TELEGRAM_PSYCHOLOGIST_ROOM = os.getenv("TELEGRAM_PSYCHOLOGIST_ROOM", None)
TELEGRAM_BROADCAST = os.getenv("TELEGRAM_BROADCAST", None)
