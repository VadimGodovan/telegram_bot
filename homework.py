import logging
import os
import requests
import time
import telegram
from requests.exceptions import RequestException

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
    """Принимает message и bot отправляет message заданному пользователю по CHAT_ID"""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.info(f'Сообщение отправлено успешно {message}')
    except Exception as error:
        error_message = (f'Не удалась отправка сообщения: {error}')
        logging.error(error_message)
        raise error(error_message)
        
    
def get_api_answer(current_timestamp):
    """Получает временную метку, отправляет к API ENDPOINT запрос и возвращает сформированный .json ответ"""
    url = ENDPOINT
    headers = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
    timestamp = current_timestamp
    params = {'from_date': timestamp }
    try:
        response = requests.get(url, headers=headers, params=params)
        logger.info('Запрос к {ENDPOINT} выполнен успешно')
    except Exception as error:
        error_message = (f'Не удалась сделать запрос к {ENDPOINT} (APIyandex): {error}')
        logging.error(error_message)
        raise error(error_message)
    if response.status_code != 200:
        error_message = 'Сервер {ENDPOINT} получает запрос, но не отвечает'
        logging.error(error_message)
        raise Exception(error_message)
    return response.json()
    
   
def check_response(response):
    """Проверяет корректность response, возвращает словарь домашней работы"""
    if not isinstance(response, dict):
        error_message = 'Ответ не является словарём'
        logging.error(error_message)
        raise TypeError(error_message)

    if ['homeworks'][0] not in response:
        error_message = 'Ответ не содержит домашней работы'
        logging.error(error_message)
        raise IndexError(error_message)
    
    try:
        homeworks = response['homeworks']
        if len(homeworks) == 0:
            raise KeyError('Ошибка, нет домашек')
        return homeworks
    except RequestException:
        raise RequestException('Ошибка запроса')
    
    #if ['homeworks'][0] in response:
        #return response['homeworks'][0]
    #if response['homeworks'] in response:
        #return response['homeworks']
    
        #return response
        
    
    #homework = response.get('homeworks')[0]
    #return homework
    
    
def parse_status(homework):
    """Извлекает из homework статус и имя домашней работы и создаёт готовую строку для отправки"""
    #if isinstance(homework, list):
        #error_message = 'Ответ не является словарём'
        #logging.error(error_message)
        #raise TypeError(error_message)
    
    try:
        homework_name = homework['homework_name']
    except KeyError as error:
        error_message = (f'Не удалось получить имя домашней работы: {error}')
        logging.error(error_message)
        raise KeyError(error_message)
    try:
        homework_status = homework['status']
    except KeyError as error:
        error_message = (f'Не удалось получить статус домашней работы: {error}')
        logging.error(error_message)
        raise KeyError(error_message)
    try:
        verdict = HOMEWORK_STATUSES[homework_status]
    except KeyError as error:
        error_message = (f'Неизвестный статус домашней работы: {error}')
        logging.error(error_message)
        raise KeyError(error_message)
    return f'Изменился статус проверки работы {homework_name}. {verdict}'


def check_tokens():
    """Проверяет доступность переменных с ключами"""
    if (PRACTICUM_TOKEN is None or 
        TELEGRAM_TOKEN is None or
        TELEGRAM_CHAT_ID is None):
        return False
    else:
        return True


def main():
    """Основная логика работы бота"""
    #остальные функции запускаются здесь
    #Сделать запрос к API.
    #Проверить ответ.
    #Если есть обновления — получить статус работы из обновления и отправить сообщение в Telegram.
    #Подождать некоторое время и сделать новый запрос.
    try:
        check_tokens()
    except Exception as error:
        logging.error(f'Ошибка в TOKEN KEY или CHAT_ID: {error}')
    bot = telegram.Bot(TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
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


if __name__ == '__main__':
    main()
