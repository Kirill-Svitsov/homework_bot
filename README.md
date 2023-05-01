Homework telegram bot description
Телеграм бот, уведомляющий о статусе домашней работы на Яндекс практикум

Как развернуть проект локально:
Установите Python 3.9
Склонируйте этот репозиторий в рабочую папку (ссылка https://github.com/Kirill-Svitsov/homework_bot)
Создайте виртуальное окружение python3 -m venv env.
Активируйте виртуальное окружение: source venv/bin/activate (Linux), venv\Scripts\activate (Windows).
Установите зависимости: pip install -r requirements.txt.
Создайте файл .env, в котором укажите необходимые переменные окружения:
(Эти переменные необходимо получить самостоятельно)
PRACTICUM_TOKEN (ссылка https://oauth.yandex.ru/authorize?
response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a.), 
TELEGRAM_TOKEN (@BotFather),
TELEGRAM_CHAT_ID (@userinfobot)
Запустите программу в терминале: python3 homework.py.
Функциональность бота:
Раз в 10 минут опрашивает API сервиса Практикум.Домашка и проверяет статус отправленной на ревью домашней работы;
При обновлении статуса анализирует ответ API и отправляет вам соответствующее уведомление в Telegram;
Логирует свою работу и сообщает вам о важных проблемах сообщением в Telegram.
Описание основных функций
send_message(bot, message) - отправляет сообщение в указанный в настройках чат в Telegram.
get_api_answer(current_timestamp) - отправляет запрос к API Яндекс.Практикум и получает данные о проверке домашней работы.
check_response(response) - проверяет корректность ответа API.
parse_status(homework) - извлекает статус проверки домашней работы и возвращает соответствующее сообщение.
check_tokens() - проверяет наличие необходимых переменных окружения.
