import os

from enum import Enum, auto
from dotenv import load_dotenv

load_dotenv()
admin_ids = os.getenv("ADMIN_IDS").split(",")

class Config:
    TELEGRAM_TOKEN: str = os.getenv('TOKEN')
    DATABASE_URL: str = os.getenv('DATABASE_URL')
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    ADMIN_IDS = admin_ids  # Add your Telegram user ID


class ConversationState(Enum):
    ADMIN = auto()
    CHOOSE_SERVICE = auto()
    PREPARE_SECTION = auto()
    ADD_SECTION = auto()
    CHOOSE_COURSE = auto()
    BLOCKCHAIN_URL = auto()
    CURRENCY = auto()
    NETWORK = auto()
    CONTRACT_ADDRESS = auto()
    TEAM = auto()
    PRIORITY = auto()
    SCREENSHOT = auto()