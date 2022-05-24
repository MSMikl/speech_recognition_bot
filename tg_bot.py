import logging
import os

from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Updater, CallbackContext, CommandHandler, MessageHandler, Filters
)

from dialog_funcs import detect_intent_text

logger = logging.getLogger('bot_logger')


def main():
    load_dotenv()
    tg_token = os.getenv('TG_TOKEN')
    project_id = os.getenv('GOOGLE_PROJECT_ID')
    updater = Updater(token=tg_token)
    dispatcher = updater.dispatcher
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    handler = RotatingFileHandler("tg_bot.log", maxBytes=200, backupCount=2)
    logger.addHandler(handler)

    def start(update: Update, context: CallbackContext):
        context.bot.sendMessage(
            chat_id=update.effective_chat.id,
            text='Здравствуйте'
        )

    def speech(update: Update, context: CallbackContext):
        message = detect_intent_text(
                project_id,
                update.effective_chat.id,
                update.message.text,
                'ru-RU'
            )
        if message:
            context.bot.sendMessage(
                chat_id=update.effective_chat.id,
                text=message
            )

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    speech_handler = MessageHandler(Filters.text & (~Filters.command), speech)
    dispatcher.add_handler(speech_handler)

    updater.start_polling()
