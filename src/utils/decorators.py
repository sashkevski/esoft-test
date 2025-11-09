import datetime
import logging
from functools import wraps


def strategy_timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        strategy_name = args[0].__class__.__name__
        logger = logging.getLogger(strategy_name)
        logger.info(f"Запуск стратегии: {strategy_name}")
        start = datetime.datetime.now()
        result = func(*args, **kwargs)
        end = datetime.datetime.now()
        delta = end - start
        logger.info(
            f"Стратегия '{strategy_name}' успешно выполнилась за {str(delta).split('.')[0]}"
        )
        return result

    return wrapper


def exceptions_handler(logger: logging.Logger):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            try:
                result = func(*args, **kwargs)
                logger.debug(f"Функция {func_name} успешно завершилась")
                return result
            except Exception as e:
                logger.error(f"Функция {func_name} предварительно завершилась с ошибкой: {e}")
                raise e

        return wrapper

    return decorator
