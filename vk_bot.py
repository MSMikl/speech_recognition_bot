import logging
import os

from logging.handlers import RotatingFileHandler
from random import randint

import vk_api as vk

from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

from dialog_funcs import detect_intent_text

logger = logging.getLogger('tbot')


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=randint(1, 1000)
    )


def main():
    load_dotenv()
    vk_token = os.getenv('VK_TOKEN')
    project_id = os.getenv('GOOGLE_PROJECT_ID')
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    handler = RotatingFileHandler("vk_bot.log", maxBytes=200, backupCount=2)
    logger.addHandler(handler)

    vk_session = vk.VkApi(token=vk_token)
    longpoll = VkLongPoll(vk_session)
    vk_api = vk_session.get_api()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            message = detect_intent_text(
                project_id,
                event.user_id,
                event.text,
                'ru-RU'
            )
            if message:
                vk_api.messages.send(
                    user_id=event.user_id,
                    message=message,
                    random_id=randint(1, 1000)
                )


if __name__ == '__main__':
    main()
