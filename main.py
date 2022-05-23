import logging
import os

from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters

from dotenv import load_dotenv

logger = logging.getLogger('tbot')

load_dotenv()
tg_token = os.getenv('TG_TOKEN')
updater = Updater(token=tg_token)
dispatcher = updater.dispatcher
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def start(update: Update, context: CallbackContext):
    context.bot.sendMessage(
        chat_id=update.effective_chat.id,
        text='Здравствуйте'
    )


def echo(update: Update, context: CallbackContext):
    context.bot.sendMessage(
        chat_id=update.effective_chat.id,
        text=update.message.text+'!!!'
    )


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()
