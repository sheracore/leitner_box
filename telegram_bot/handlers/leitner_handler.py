import os
import csv
import logging

from enum import Enum

from requests import session

from telegram_bot import Dictionary
from telegram_bot.utils import save_file, remove_file

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler, CallbackContext
from telegram_bot.config.config import ConversationState, Config
from telegram_bot.core.db import Database
from telegram_bot.models import Course, Section, LanguageChoice, SectionDictionary, User

# Set up logging to monitor database connection issues
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AdminServices(Enum):
    ADD_COURSE = "ADD_OR_UPDATE_COURSE"


class LeitnerHandler:

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            db = Database.get_db()
            session = next(db)

            first_name = update.message.from_user.first_name
            last_name = update.message.from_user.last_name
            username = update.effective_user.name
            user_id = str(update.effective_user.id)

            if not session.query(User).filter_by(user_id=user_id).first():
                session.add(User(first_name=first_name, last_name=last_name, username=username, user_id=user_id))
                session.commit()

            start_text = (
            f"کاربر {first_name} عزیز به لایتنر باکس خوش آمدید.\n\n"
            "🚀 از دستور /start برای شروع دوباره استفاده کنید.\n"
            "ℹ️ از دستور /help برای آموزش استفاده از لایتنر باکس استفاده کنید.\n"
            "⚙️ از دستور /setting برای مدیریت لایتنرتان استفاده کنید.\n"
        )
            if str(user_id) in Config.ADMIN_IDS:
                start_text += "👑 از دستور /admin برای مدیریت دوره ها توسط ادمین استفاده کنید.\n"
                start_text += "❌ از دستور /close برای خاتمه به مکالمه فعلی.\n"

            await update.message.reply_text(start_text)


        except Exception as e:
            logger.error(e)
            await update.message.reply_text(f"خطایی رخ داده لطفا بعدا تلاش کنید و به ادمین اطلاع بدهید: {e}")

    async def close(self, update: Update, context: CallbackContext) -> int:
        await update.message.reply_text("مکالمه فعلا به پایان رسید برای شروع دباره /start را بزنید")
        return ConversationHandler.END

    async def help(self, update: Update, context: CallbackContext) -> None:
        await update.message.reply_text("این راهنمای استفاده از لایتنر باکسه")

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
            "لطفا یکی از خدمت ها را انتخاب کنید",
            reply_markup=reply_markup
        )
        return ConversationState.CHOOSE_SERVICE.value

    async def choose_service(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        if update.message.text == AdminServices.ADD_COURSE.value:
            try:
                db = Database.get_db()
                session = next(db)
                courses = session.query(Course.name).all()
                courses = [[name[0]] for name in courses]
                reply_markup = ReplyKeyboardMarkup(courses,
                                                   resize_keyboard=True,
                                                   one_time_keyboard=True)

                await update.message.reply_text("لطفا یک دوره را انتخاب کنید یا اسم دوره جدید وارد کنید:",
                                                reply_markup=reply_markup)
                return ConversationState.PREPARE_SECTION.value
            except Exception as e:
                logger.error(e)
                await update.message.reply_text(f"Error: {str(e)}")
                return ConversationHandler.END

        return ConversationHandler.END

    async def prepare_section(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        try:
            db = Database.get_db()
            session = next(db)

            course = update.message.text
            course_obj = session.query(Course).filter_by(name=course).first()
            if not course_obj:
                course_obj = Course(name=course)
                session.add(course_obj)
                session.commit()

            context.user_data['course_obj'] = course_obj
            sections = session.query(Section.name).filter_by(course_id=course_obj.id).all()
            sections = [[name[0]] for name in sections]
            if not sections:
                await update.message.reply_text("یک بخش جدید وارد کنید(برای مثلا Oxford intermediate) برای دوره Oxford", reply_markup=ReplyKeyboardRemove())
                return ConversationState.ADD_SECTION.value

            reply_markup = ReplyKeyboardMarkup(
                sections,
                one_time_keyboard=True,
                resize_keyboard=True)

            await update.message.reply_text(
                "یک بخش جدید وارد کنید یا بین یخش های زیر یک بخش را برای ادیت کردن آن انتخاب کنید",
                reply_markup=reply_markup)

            return ConversationState.ADD_SECTION.value

        except Exception as e:
            logger.error(e)
            await update.message.reply_text(f"Error: {str(e)}")
            return ConversationHandler.END

    async def add_section(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        try:
            db = Database.get_db()
            session = next(db)

            section_name = update.message.text
            course_obj = context.user_data['course_obj']
            section_obj = session.query(Section).filter_by(name=section_name, course_id=course_obj.id).first()
            if not section_obj:
                section_obj = Section(name=section_name, course_id=course_obj.id)
                session.add(section_obj)
                session.commit()
            context.user_data['section_obj'] = section_obj

            dictionary_file_path = "dictionary_sample.csv"
            with open(dictionary_file_path, "rb") as file:
                await update.message.reply_document(
                    document=file,
                    filename=os.path.basename(dictionary_file_path),
                    caption=f"Dictionary csv file Sample"
                )

            await update.message.reply_text(
                f"Section: {section_obj.name}. حالا فایل csv برای پر کردن دیکشنری های بخش را همانند فایل نمونه ضمیمه شده ارسال کنید",
                reply_markup=ReplyKeyboardRemove())
            return ConversationState.PREPARE_DICTIONARY.value

        except Exception as e:
            logger.error(e)
            await update.message.reply_text(f"Error: {str(e)}")
            return ConversationHandler.END

    async def prepare_dictionary(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        file_name = None
        try:
            db = Database.get_db()
            session = next(db)

            # Get the file from Telegram
            document = update.message.document
            file = await document.get_file()
            file_content = await file.download_as_bytearray()

            # Save the file and get the file path
            course_obj = context.user_data['course_obj']
            section_obj = context.user_data['section_obj']
            file_name = f"{course_obj.name}_{section_obj.name}_{document.file_name}"
            file_path = save_file(file_content, file_name)
            context.user_data['file_path'] = file_path

            # Update the Section with the file path
            section = session.query(Section).filter(Section.id == section_obj.id).first()
            if not section:
                await update.message.reply_text("Section not found.")
                return ConversationHandler.END

            remove_file(section.dictionary_file_path)
            section.dictionary_file_path = file_path
            session.commit()
            await self._parse_dictionary_file(session, file_path, section_obj)
            await update.message.reply_text(f"فال با موقعیت آپلود و پارس شد: {section.name}!")

            return ConversationHandler.END

        except Exception as e:
            logger.error(e)
            await update.message.reply_text(f"Error: {str(e)}")
            if file_name:
                remove_file(file_name)
            return ConversationHandler.END

    async def _parse_dictionary_file(self, session, file_path: str, section_obj: Section) -> None:
        try:
            with open(file_path, "r") as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)  # Skip the header row
                for row in csv_reader:
                    try:
                        word = row[0]
                        meaning = row[1]
                        # TODO: add examples

                        dictionary_obj = session.query(Dictionary).filter_by(word=word, language=LanguageChoice.EN).first()
                        if not dictionary_obj:
                            dictionary_obj = Dictionary(word=word, meaning=meaning, language=LanguageChoice.EN)
                            session.add(dictionary_obj)
                            session.commit()

                        session.add(SectionDictionary(section_id=section_obj.id, dictionary_id=dictionary_obj.id))
                        session.commit()
                    except Exception as e:
                        logger.error(e)
                        raise Exception(f"Unsuccessful adding dictionary: {row[0]} with error: {str(e)}")

        except Exception as e:
            logger.error(e)
            raise Exception(f"Dictionary csv file can't be parsed: {str(e)}")