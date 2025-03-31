from telegram_bot.core.db import Database
import telegram_bot
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Telegram Bot CLI")
    parser.add_argument("command", choices=["migrate", "run"], help="Command to execute")
    args = parser.parse_args()

    if args.command == 'run':
        print('telegram_bot()')
    elif args.command == 'migrate':
        Database.migrate()
