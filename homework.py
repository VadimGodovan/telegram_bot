import os

import requests

from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater

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
    #отправляет сообщение в Telegram чат, определяемый переменной окружения TELEGRAM_CHAT_ID. 
    # Принимает на вход два параметра: экземпляр класса Bot и строку с текстом сообщения.
    ...


def get_api_answer(current_timestamp):
    # Делаем GET-запрос к эндпоинту url с заголовком headers и параметрами params
    # Печатаем ответ API в формате JSON
    # А можно ответ в формате JSON привести к типам данных Python и напечатать и его
    # print(homework_statuses.json()) 
    
    # делает запрос к единственному эндпоинту API-сервиса. 
    # В качестве параметра функция получает временную метку. 
    # В случае успешного запроса должна вернуть ответ API, преобразовав 
    # его из формата JSON к типам данных Python
    url = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
    headers = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
    timestamp = current_timestamp or int(time.time(0))
    params = {'from_date': timestamp}
    homework_statuses = requests.get(url, headers=headers, params=params)
    response = (homework_statuses.json())
    
    return response
    
    #result_status = result_status["homeworks"][0]
    #итоговый статус
    #pprint(result_status['status'])
    


def check_response(response):
    #проверяет ответ API на корректность. В качестве параметра функция получает ответ API,
    #приведенный к типам данных Python. Если ответ API 
    # соответствует ожиданиям, то функция должна вернуть список домашних работ 
    #(он может быть и пустым), доступный в ответе API по ключу 'homeworks'.
    ...


def parse_status(homework):
    #извлекает из информации о конкретной домашней работе статус этой работы. 
    # В качестве параметра функция получает только один элемент из списка домашних работ. 
    # В случае успеха, функция возвращает подготовленную для отправки в Telegram строку, 
    # содержащую один из вердиктов словаря HOMEWORK_STATUSES
    homework_name = ...
    homework_status = ...

    ...

    verdict = ...

    ...

    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    # проверяет доступность переменных окружения, которые необходимы для работы программы. 
    # Если отсутствует хотя бы одна переменная окружения — 
    # функция должна вернуть False, иначе — True.
    if PRACTICUM_TOKEN == os.getenv('PRACTIC_TOKEN_KEY') and TELEGRAM_TOKEN == os.getenv('TELEG_TOKEN_KEY') and TELEGRAM_CHAT_ID == os.getenv('TELEG_CHAT_ID_KEY'):
        return True
    else:
        return False


def main():
    """Основная логика работы бота."""
    #остальные функции запускаются здесь
    #Сделать запрос к API.
    #Проверить ответ.
    #Если есть обновления — получить статус работы из обновления и отправить сообщение в Telegram.
    #Подождать некоторое время и сделать новый запрос.

    ...

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())

    ...

    while True:
        try:
            response = ...

            ...

            current_timestamp = ...
            time.sleep(RETRY_TIME)

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            ...
            time.sleep(RETRY_TIME)
        else:
            ...


if __name__ == '__main__':
    main()
