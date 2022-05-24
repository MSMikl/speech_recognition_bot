import logging
import os

from google.cloud import dialogflow
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters

from dotenv import load_dotenv

logger = logging.getLogger('tbot')

load_dotenv()
tg_token = os.getenv('TG_TOKEN')
project_id = os.getenv('GOOGLE_PROJECT_ID')
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


def detect_intent_text(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
    return response.query_result.fulfillment_text


def speech(update: Update, context: CallbackContext):
    context.bot.sendMessage(
        chat_id=update.effective_chat.id,
        text=detect_intent_text(
            project_id,
            update.effective_chat.id,
            update.message.text,
            'ru-RU'
        )
    )


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

speech_handler = MessageHandler(Filters.text & (~Filters.command), speech)
dispatcher.add_handler(speech_handler)

updater.start_polling()
