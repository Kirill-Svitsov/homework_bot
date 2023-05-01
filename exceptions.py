class EndpointError(Exception):
    """Недоступен Эндпоинт."""
    pass


class SendMessageException(Exception):
    """Ошибка отправки сообщения в TELEGRAM."""
    pass


class JsonError(Exception):
    """Невозможно получить данные в JSON"""
    pass


class StatusCodeException(Exception):
    """Статус код ответа != 200"""
    pass
