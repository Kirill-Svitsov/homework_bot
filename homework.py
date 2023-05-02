import logging
import os
import sys
import time
from http import HTTPStatus
from logging import Formatter, StreamHandler

import requests
import simplejson
import telegram
from dotenv import load_dotenv

import exceptions

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
tokens = [
    'PRACTICUM_TOKEN',
    'TELEGRAM_TOKEN',
    'TELEGRAM_CHAT_ID',
]
RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logging.basicConfig(
    level=logging.DEBUG,
    filename='main.log',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)


def check_tokens():
    """Проверка наличия всех токенов."""
    if not PRACTICUM_TOKEN:
        logger.critical('Отсутствует токен: "PRACTICUM_TOKEN"')
        return False

    if not TELEGRAM_TOKEN:
        logger.critical('Отсутствует токен: "TELEGRAM_TOKEN"')
        return False

    if not TELEGRAM_CHAT_ID:
        logger.critical('Отсутствует телеграм id: "TELEGRAM_CHAT_ID"')
        return False
    return True


def send_message(bot, message):
    """Отправка сообщения в телеграмм."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.debug('Бот отправил сообщение в чат')
    except telegram.error.TelegramError as error:
        logger.error(f'Сбой при отправке сообщения в чат - {error}')
        raise exceptions.SendMessageException('Ошибка отправки сообщения')


def get_api_answer(timestamp):
    """Делает запрос к API яндекса."""
    payload = {'from_date': timestamp}
    try:
        homework_statuses = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params=payload,
        )
    except requests.exceptions.RequestException as error:
        raise exceptions.EndpointError(f'Ошибка при запросе к API: {error}')
    if homework_statuses.status_code != HTTPStatus.OK:
        raise exceptions.StatusCodeException(
            'HTTP статус ответа API != 200'
        )
    try:
        return homework_statuses.json()
    except simplejson.errors.JSONDecodeError:
        raise exceptions.JsonError('Невозможно получить данные в JSON')


def check_response(response):
    """Проверяет ответ API на соответствие документации."""
    if not isinstance(response, dict):
        raise TypeError('response не соответствует документации')
    if 'homeworks' not in response:
        raise KeyError('Отсутствует ключ homeworks')
    if 'current_date' not in response:
        raise KeyError('Отсутствует ключ current_date')
    if not isinstance(response['homeworks'], list):
        raise TypeError('Данные переданы не в виде списка')
    if not response.get('homeworks'):

        raise IndexError('Список с домашними работами пуст')
    return response.get('homeworks')


def parse_status(homework):
    """Извлекает статус домашней работы."""
    try:
        homework_name = homework['homework_name']
    except KeyError:
        raise KeyError('Отсутствует ключ "homework_name"')
    hw_status = homework.get('status')
    if hw_status not in HOMEWORK_VERDICTS:
        raise KeyError('Статуса нет в словаре вердиктов')
    if homework['status'] in HOMEWORK_VERDICTS:
        verdict = HOMEWORK_VERDICTS[homework['status']]
        return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    if check_tokens():
        logging.info('Бот запущен.')
        bot = telegram.Bot(token=TELEGRAM_TOKEN)
        timestamp = 0
        first_status = ''
        error_message = ''
        while True:
            try:
                response = get_api_answer(timestamp)
                check_response(response)
                logger.info('Cписок работ получен.')
                new_status = parse_status(response['homeworks'][0])
                if new_status != first_status:
                    send_message(bot, new_status)
                first_status = new_status
            except Exception as error:
                message = f'Сбой в работе программы: {error}'
                logger.error(message)
                if message != error_message:
                    send_message(bot, message)
                error_message = message
            finally:
                timestamp = response['current_date']
                time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
