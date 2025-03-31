import argparse

from telegram_bot.core.db import Database
from telegram_bot.start import run

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Telegram Bot CLI")
    parser.add_argument("command", choices=["migrate", "run"], help="Command to execute")
    args = parser.parse_args()

    if args.command == 'run':
        run()
    elif args.command == 'migrate':
        Database.migrate()
