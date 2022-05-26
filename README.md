# speech_recognition_bot
 
Учебный проект - чат-бот с использованием сервиса распознавания речи [DialogFlow](https://dialogflow.cloud.google.com/)

Представляет собой двух ботов - Вконтакте и Телеграм - обрабатывающих типичные вопросы покупателей книжного магазина.

Распространяется в виде докер-контейнеров

## Установка

Предусмотрены два варианта

- запуск готовых docker-контейнеров
- самостоятельный запуск кода

## 1. Docker

Необходимо разворачивать на машине с установленным Docker и Docker-Compose

Скачать из репозитория файл `example_docker-compose.yml`, переименовать его в `docker-compose.yml`, заменить в нем указанный в фигруных скобках собственными значениями секретных ключей:

      TG_TOKEN: {Токен телеграм-бота}
      TG_USER: {id пользователя Телеграм для доставки системных уведомлений}
      GOOGLE_PROJECT_ID: {id проекта DialogFlow}
      GOOGLE_APPLICATION_CREDENTIALS: /config/google_auth.json
      VK_TOKEN: {Токен API группы Вконтакте}
    volumes:
      - {Путь к файлу авторизации DialogFlow}:/config/google_auth.json
      
Выполнить команду 'docker-compose up -d'

Образы будут скачаны из репозитория и запущены в виде двух контейнеров.

## 2. Самостоятельный запуск кода

Необходимо запускать на системе с установленным python

Скачать файлы из репозитория, создать файл `.env`, в который внести следующие переменные:

      TG_TOKEN = {Токен телеграм-бота}
      TG_USER = {id пользователя Телеграм для доставки системных уведомлений}
      GOOGLE_PROJECT_ID = {id проекта DialogFlow}
      GOOGLE_APPLICATION_CREDENTIALS = {Путь к файлу авторизации DialogFlow}
      VK_TOKEN = {Токен API группы Вконтакте}
      
Для обучения DialogFlow набору стандартных запросов из файла `questions.json` один раз следует выполнить команду

    pythion create_intents.py
    
Команда для запуска телеграм-бота 

    python tg_bot.py
    
Команда для запуска бота Вконтакте

    python vk_bot.py

## Использование

С работой ботов можно ознакомиться на рабочих примерах.

[Бот в телеграм](https://telegram.me/voice_rceo_bot)

[Бот Вконтакте](https://vk.com/im?sel=-213499802)

Боты отвечают на приветствия, а также на следующие вопросы:

- Вопросы от действующих партнёров
- Вопросы от забаненных
- Забыл пароль
- Привет
- Удаление аккаунта
- Устройство на работу

Нейросеть распознает различные формулировки вопросов. Если вопрос не распознан, то бот не ответит - в этом случае стоит попробовать повторить вопрос в другой формулировке.
