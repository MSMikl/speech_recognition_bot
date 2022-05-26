import logging
import os

from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import (
    Updater, CallbackContext, CommandHandler, MessageHandler, Filters
)

from dialog_funcs import detect_intent_text

logger = logging.getLogger('bot_logger')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_token, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.logger_bot = Bot(token=tg_token)

    def emit(self, record):
        log_entry = self.format(record)
        self.logger_bot.send_message(chat_id=self.chat_id, text=log_entry)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Здравствуйте'
    )


def speech(update: Update, context: CallbackContext):
    message = detect_intent_text(
            context.bot_data.get('project_id'),
            update.effective_chat.id,
            update.message.text,
            'ru-RU'
        )
    if message:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message
        )


def main():
    load_dotenv()
    tg_token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_USER')
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
