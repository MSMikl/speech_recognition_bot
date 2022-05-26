import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Updater, CallbackContext, CommandHandler, MessageHandler, Filters
)

from dialog_funcs import detect_intent_text
from tg_logging_handler import TelegramLogsHandler


logger = logging.getLogger('bot_logger')


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Здравствуйте'
    )


def speech(update: Update, context: CallbackContext):
    message, _ = detect_intent_text(
            context.bot_data.get('project_id'),
            update.effective_chat.id,
            update.message.text,
            'ru-RU'
        )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message
    )


def main():
    load_dotenv()
    tg_token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_USER_ID')
    project_id = os.getenv('GOOGLE_PROJECT_ID')
    updater = Updater(token=tg_token)

    dispatcher = updater.dispatcher
    dispatcher.bot_data['project_id'] = project_id

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger.addHandler(TelegramLogsHandler(tg_token, chat_id))

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    speech_handler = MessageHandler(
        Filters.text & (~Filters.command),
        speech
    )
    dispatcher.add_handler(speech_handler)

    logger.info('Бот стартует')
    updater.start_polling()


if __name__ == '__main__':
    main()
