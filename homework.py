import logging
import os
import time

import requests
import telegram
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


logging.basicConfig(
    format='%(asctime)s, %(levelname)s,%(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


def send_message(bot, message):
    """Отправляет message заданному пользователю по CHAT_ID."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.info(f'Сообщение отправлено успешно {message}')
    except Exception as error:
        error_message = (f'Не удалась отправка сообщения: {error}')
        logging.error(error_message)
        raise error(error_message)


def get_api_answer(current_timestamp):
    """Отправляет к API ENDPOINT запрос возвращает сформированный ответ."""
    url = ENDPOINT
    headers = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
    timestamp = current_timestamp
    params = {'from_date': timestamp}
    try:
        response = requests.get(url, headers=headers, params=params)
        logger.info('Запрос к {ENDPOINT} выполнен успешно')
    except Exception as error:
        error_message = (f'Не удалась сделать запрос к APIyandex {error}')
        logging.error(error_message)
        raise error(error_message)
    if response.status_code != 200:
        error_message = 'Сервер {ENDPOINT} получает запрос, но не отвечает'
        logging.error(error_message)
        raise Exception(error_message)
    return response.json()


def check_response(response):
    """Проверяет корректность response, возвращает словарь домашней работы."""
    if not response:
        raise TypeError('Пустой ответ')
    if not isinstance(response, dict):
        raise TypeError('Ожидаем словарь')
    if not isinstance(response.get('homeworks'), list):
        raise TypeError('Ожидаем список')
    return response.get('homeworks')


def parse_status(homework):
    """Извлекает из homework статус и имя домашней работы."""
    homework_name = homework['homework_name']
    homework_status = homework['status']
    if homework_status in HOMEWORK_STATUSES:
        return f'Изменился статус домашней работы "{homework_name}".' \
               f' {HOMEWORK_STATUSES[homework_status]}'
    else:
        raise ValueError('Не удалось определить статус домашней работы')


def check_tokens():
    """Проверяет доступность переменных с ключами."""
    list = [PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]
    for key in list:
        if key is None:
            return False
    else:
        return True


def main():
    """Основная логика работы бота."""
    try:
        check_tokens()
    except Exception as error:
        logging.error(f'Ошибка в TOKEN KEY или CHAT_ID: {error}')
    bot = telegram.Bot(TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    while True:
        try:
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
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
