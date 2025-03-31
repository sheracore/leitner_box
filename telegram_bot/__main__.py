import os
import dotenv

dotenv.load_dotenv()
os.environ['http_proxy'] = 'http://127.0.0.1:2081'
os.environ['https_proxy'] = 'http://127.0.0.1:2081'

from telegram import Update
from telegram.ext import (Application, CommandHandler, ConversationHandler, MessageHandler, CallbackQueryHandler,
                          filters, CallbackContext)
from config.config import Config
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Define states
RP, START, PD, SAVE = range(4)


def leitner_conversation():
    return ConversationHandler(
        entry_points=[CommandHandler('start', start),
                      CommandHandler('help', help_command)],
        states={
            RP: [MessageHandler(filters.TEXT & ~filters.COMMAND, rp)],
            PD: [MessageHandler(filters.TEXT & ~filters.COMMAND, pd)],
            SAVE: [MessageHandler(filters.TEXT & ~filters.COMMAND, save)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

async def rp(update: Update, context: CallbackContext):
    new_word = update.message.text
    if new_word == 'skip':
        await update.message.reply_text("Inter your last word")
        return PD
    if context.user_data.get('word'):
        context.user_data['word'].append(new_word)
    else:
        context.user_data['word'] = [new_word]
    await update.message.reply_text("Insert new word or type `skip`")
    return RP

async def start(update, context):
    await update.message.reply_text("please inter your data")
    return RP


async def help_command(update, context):
    await update.message.reply_text("You can use /start to interact with me.")


async def pd(update, context):
    user_data = update.message.text
    context.user_data['pd'] = user_data
    await update.message.reply_text("inter save data location")
    return SAVE

async def save(update, context):
    saving_data = update.message.text
    context.user_data['save'] = saving_data
    await update.message.reply_text(f"saving data in {context.user_data['save']} with data: {context.user_data['pd']}, {context.user_data['word']}")


async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("The conversation has been canceled. See you next time!")
    return ConversationHandler.END


def main():
    app = (
        Application.builder()
        .token(Config.TELEGRAM_TOKEN)
        .connect_timeout(20.0)
        .read_timeout(20.0)
        .write_timeout(20.0)
        .pool_timeout(3.0)
        .connection_pool_size(8)
        .get_updates_connect_timeout(30.0)
        .get_updates_read_timeout(30.0)
        .get_updates_write_timeout(30.0)
        .get_updates_pool_timeout(3.0)
        .get_updates_connection_pool_size(8)
        .concurrent_updates(True)
        .build()
    )

    app.add_handler(leitner_conversation())

    app.run_polling()


if __name__ == "__main__":
    dotenv.load_dotenv()

    main()
