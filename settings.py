import os
from dotenv import load_dotenv
load_dotenv()
# Telegram token
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
# Security tokens
SERVER_TOKEN = os.getenv("SERVER_TOKEN", "")
# Sever url
SERVER_URL = os.getenv("SERVER_URL", "")
# instance name + url
INSTANCE_URL = os.getenv("INSTANCE_URL")
