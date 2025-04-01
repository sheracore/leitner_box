from enum import Enum
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram_bot.config.config import ConversationState, Config
from telegram_bot.core.db import Database
from telegram_bot.models.section import Section


class AdminServices(Enum):
    ADD_COURSE = "ADD_COURSE"


class LeitnerHandler:

    async def admin(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user_id = update.effective_user.id
        if str(user_id) not in Config.ADMIN_IDS:
            await update.message.reply_text("You are not authorized to use this command.")
            return ConversationHandler.END

        admin_service_list = [[service.value] for service in AdminServices]
        reply_markup = ReplyKeyboardMarkup(
            admin_service_list,
            one_time_keyboard=True,
            resize_keyboard=True)

        await update.message.reply_text(
            "Please choose between services",
            reply_markup=reply_markup
        )
        return ConversationState.CHOOSE_SERVICE.value

    async def choose_service(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        if update.message.text == AdminServices.ADD_COURSE.value:
            # # -------------------------------------------------
            # keyboard = [
            #     [
            #         InlineKeyboardButton("Option 1", callback_data="option1"),
            #         InlineKeyboardButton("Option 2", callback_data="option2"),
            #     ]
            # ]
            # reply_markup = InlineKeyboardMarkup(keyboard)
            #
            # # Send a message with the Inline Keyboard
            # await update.message.reply_text("Choose an option:", reply_markup=reply_markup)
            # # -------------------------------------------------

            try:
                db = Database.get_db()
                session = next(db)
                sections = session.query(Section.name).all()

                sections = [[name[0]] for name in sections]
                reply_markup = ReplyKeyboardMarkup(sections,
                                                   resize_keyboard=True,
                                                   one_time_keyboard=True)

                await update.message.reply_text("Select between Course names of input new Course",
                                                reply_markup=reply_markup)
            except Exception as e:
                await update.message.reply_text(f"Error: {str(e)}")

    async def choose_section(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        db = Database.get_db()
        session = next(db)
        try:
            sections = session.query(Section).all()
            section_list = "\n".join([f"ID: {section.id}, Name: {section.name}" for section in sections])
            await update.message.reply_text(f"Sections:\n{section_list}")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")

        await update.message.reply_text("Keyboard removed!", reply_markup=ReplyKeyboardRemove())

        return ConversationState.ADD_COURSE.value
        # await update.message.reply_text("Please enter the section name of choose between these sections",
        #                                 reply_markup=)
