import os
import dotenv

from telegram_bot.handlers.leitner_handler import LeitnerHandler
from telegram_bot.config.config import ConversationState

dotenv.load_dotenv()
os.environ['http_proxy'] = 'http://127.0.0.1:2081'
os.environ['https_proxy'] = 'http://127.0.0.1:2081'

from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters, CallbackQueryHandler

from telegram_bot.config.config import Config


def leitner_conversation(leitner_handler: LeitnerHandler):
    return ConversationHandler(
        entry_points=[CommandHandler('start', leitner_handler.start),
                      CommandHandler('help', leitner_handler.help),
                      CommandHandler('admin', leitner_handler.admin),
                      ],
        states={

            ConversationState.CHOOSE_SERVICE.value: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, leitner_handler.choose_service)],

            ConversationState.PREPARE_SECTION.value: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, leitner_handler.prepare_section)],

            ConversationState.ADD_SECTION.value: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, leitner_handler.add_section)],

            ConversationState.PREPARE_DICTIONARY.value: [
                MessageHandler(filters.Document.ALL, leitner_handler.prepare_dictionary)],

            ConversationState.START_SECTIONS.value: [
                CallbackQueryHandler(leitner_handler.courses, pattern='^courses'),
                CallbackQueryHandler(leitner_handler.user_leitner_setting, pattern='^user_leitner_setting'),
                CallbackQueryHandler(leitner_handler.leitner_review, pattern='^leitner_review')
            ],

            ConversationState.COURSE.value: [
                CallbackQueryHandler(leitner_handler.course, pattern='^course_')],

            ConversationState.UPDATE_LEITNER.value: [
                CallbackQueryHandler(leitner_handler.update_leitner, pattern='^section_'),
                CallbackQueryHandler(leitner_handler.courses, pattern='^courses')],

            ConversationState.USER_LEITNER_SETTING.value: [
                CallbackQueryHandler(leitner_handler.user_leitner_setting_action, pattern='^leitner_setting')],

            ConversationState.LEITNER_REVIEW.value: [
                CallbackQueryHandler(leitner_handler.leitner_review, pattern='^leitner_action')],

        },
        fallbacks=[CommandHandler('close', leitner_handler.close)],
        allow_reentry=True
    )


def run():
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

    leitner_handler = LeitnerHandler()
    app.add_handler(leitner_conversation(leitner_handler))

    app.run_polling()
