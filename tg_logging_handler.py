import logging

from telegram import Bot


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_token, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.logger_bot = Bot(token=tg_token)

    def emit(self, record):
        log_entry = self.format(record)
        self.logger_bot.send_message(chat_id=self.chat_id, text=log_entry)
