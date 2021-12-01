import os

import requests

from telegram import ReplyKeyboardMarkup, Bot
from telegram.ext import CommandHandler, Updater
from telegram import Bot, error
import telegram 
import time
from dotenv import load_dotenv 


load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTIC_TOKEN_KEY')
TELEGRAM_TOKEN = os.getenv('TELEG_TOKEN_KEY')
TELEGRAM_CHAT_ID = os.getenv('TELEG_CHAT_ID_KEY')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def send_message(bot, message):
    """Принимает bot, message и отправляет заданному пользователю CHAT_ID"""
    bot.send_message(TELEGRAM_CHAT_ID, message)

    
def get_api_answer(current_timestamp):
    # делает запрос к единственному эндпоинту API-сервиса. 
    # В качестве параметра функция получает временную метку. 
    # В случае успешного запроса должна вернуть ответ API, преобразовав 
    # его из формата JSON к типам данных Python
    url = ENDPOINT
    headers = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
    timestamp = current_timestamp
    params = {'from_date': timestamp }
    homework_statuses = requests.get(url, headers=headers, params=params)
    return (homework_statuses.json())
    
def check_response(response):
    # проверяет ответ API на корректность. В качестве параметра функция получает ответ API, приведенный к типам данных Python.
    # Если ответ API соответствует ожиданиям, то функция должна вернуть список домашних работ 
    # (он может быть и пустым), доступный в ответе API по ключу 'homeworks'.
    try:
        response = response
    except TypeError as error:
        if not response:
            print(f'Словарь пустой {error}')
    except KeyError as error:
        if response.get('homeworks') not in response:
            print(f'Словаре отсутствует ключ "homeworks" {error}')
    else:
        return (response.get('homeworks'))

def parse_status(homework):
    #извлекает из информации о конкретной домашней работе статус этой работы. 
    # В качестве параметра функция получает только один элемент из списка домашних работ. 
    # В случае успеха, функция возвращает подготовленную для отправки в Telegram строку, 
    # содержащую один из вердиктов словаря HOMEWORK_STATUSES
    homework = homework[0]
    homework_name = homework['homework_name']
    homework_status = homework['status']
    #...
    verdict = HOMEWORK_STATUSES[homework_status]
    return f'Изменился статус проверки работы {homework_name}. {verdict}'


def check_tokens():
    # проверяет доступность переменных окружения, которые необходимы для работы программы. 
    # Если отсутствует хотя бы одна переменная окружения — 
    # функция должна вернуть False, иначе — True.
    if (PRACTICUM_TOKEN is None or 
        TELEGRAM_TOKEN is None or
        TELEGRAM_CHAT_ID is None):
        return False
    else:
        return True


def main():
    """Основная логика работы бота."""
    #остальные функции запускаются здесь
    #Сделать запрос к API.
    #Проверить ответ.
    #Если есть обновления — получить статус работы из обновления и отправить сообщение в Telegram.
    #Подождать некоторое время и сделать новый запрос.
    check_tokens()
    bot = telegram.Bot(TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    #...
    while True:
        try:
            current_timestamp = 0
            response = get_api_answer(current_timestamp)
            print(response)
            homework = check_response(response)
            print(homework)
            message = parse_status(homework)
            print(message)
            send_message(bot, message)

            current_timestamp = 0
            time.sleep(RETRY_TIME)

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            #...
            time.sleep(RETRY_TIME)
        else:
            send_message(bot, message)


if __name__ == '__main__':
    main()
