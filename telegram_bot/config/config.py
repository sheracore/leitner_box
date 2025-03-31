import os

from enum import Enum, auto
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_TOKEN: str = os.getenv('TOKEN')
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/dbname"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"


class ConversationState(Enum):
    WAITING_FOR_CHOICE = auto()
    DESCRIPTION = auto()
    ADDRESS = auto()
    BLOCKCHAIN_URL = auto()
    CURRENCY = auto()
    NETWORK = auto()
    CONTRACT_ADDRESS = auto()
    TEAM = auto()
    PRIORITY = auto()
    SCREENSHOT = auto()