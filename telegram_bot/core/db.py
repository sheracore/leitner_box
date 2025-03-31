from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
print(sys.path)
from telegram_bot.config.config import Config
from telegram_bot.models.base import Base

engine = create_engine(Config.DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Database:
    @classmethod
    def migrate(cls):
        Base.metadata.create_all(bind=engine)
        print("Migrate Done!")

    @classmethod
    def get_db(cls):
        db = Session()
        try:
            yield db
        finally:
            db.close()

