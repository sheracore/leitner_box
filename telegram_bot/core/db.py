import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from telegram_bot.config.config import Config
from telegram_bot.models.base import Base

# Set up logging to monitor database connection issues
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine(Config.DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Database:
    @classmethod
    def migrate(cls):
        Base.metadata.create_all(bind=engine)
        print("Migrate Done!")

    @classmethod
    def get_db(cls):
        db = None
        try:
            db = Session()
            yield db # for automatically close the session after each handler
        except Exception as e:
            logger.error(f"Failed to connect to database: {str(e)}")
            raise Exception("Failed to connect to database")
        finally:
            if db:
                db.close()
                logger.info("Database session closed.")

