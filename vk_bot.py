import logging
import os

import vk_api

from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

from dialog_funcs import detect_intent_text

logger = logging.getLogger('tbot')

load_dotenv()
vk_token = os.getenv('VK_TOKEN')
phone_number = os.getenv('PHONE_NUMBER')
vk_password = os.getenv('VK_PASSWORD')
project_id = os.getenv('GOOGLE_PROJECT_ID')
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

vk_session = vk_api.VkApi(token=vk_token)
longpoll = VkLongPoll(vk_session)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        print('Новое сообщение:')
        if event.to_me:
            print('Для меня от: ', event.user_id)
            print(
                'От меня для: ',
                event.user_id,
                '\n {}'.format(detect_intent_text(
                    project_id,
                    event.user_id,
                    event.text,
                    'ru-RU'
                ))
            )
        else:
            print('От меня для: ', event.user_id)
        print('Текст:', event.text)