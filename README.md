# Homework Telegram Bot Description

Телеграм бот, уведомляющий о статусе домашней работы на Яндекс Практикум.

## Развертывание проекта локально

1. Убедитесь, что у вас установлен Python 3.9.

2. Склонируйте этот репозиторий в рабочую папку:
git clone https://github.com/Kirill-Svitsov/homework_bot

3. Создайте виртуальное окружение:
- Для Linux:
  ```
  python3 -m venv env
  ```
- Для Windows:
  ```
  python -m venv env
  ```

4. Активируйте виртуальное окружение:
- Для Linux:
  ```
  source env/bin/activate
  ```
- Для Windows:
  ```
  .\env\Scripts\activate
  ```

5. Установите зависимости:
pip install -r requirements.txt

6. Создайте файл `.env` и укажите в нем необходимые переменные окружения (Эти переменные необходимо получить самостоятельно):
- `PRACTICUM_TOKEN` (ссылка: https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a)
- `TELEGRAM_TOKEN` (@BotFather)
- `TELEGRAM_CHAT_ID` (@userinfobot)

7. Запустите программу в терминале:
python3 homework.py

## Функциональность бота

- Раз в 10 минут опрашивает API сервиса Практикум.Домашка и проверяет статус отправленной на ревью домашней работы.
- При обновлении статуса анализирует ответ API и отправляет вам соответствующее уведомление в Telegram.
- Логирует свою работу и сообщает вам о важных проблемах сообщением в Telegram.

## Описание основных функций

- `send_message(bot, message)`: отправляет сообщение в указанный в настройках чат в Telegram.
- `get_api_answer(current_timestamp)`: отправляет запрос к API Яндекс.Практикум и получает данные о проверке домашней работы.
- `check_response(response)`: проверяет корректность ответа API.
- `parse_status(homework)`: извлекает статус проверки домашней работы и возвращает соответствующее сообщение.
- `check_tokens()`: проверяет наличие необходимых переменных окружения.
