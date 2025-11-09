import argparse

from config import config


def create_global_parser():
    """Создает парсер с глобальными аргументами"""

    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Показать эту справку и выйти",
    )

    log_level_group = parser.add_mutually_exclusive_group()
    log_level_group.add_argument(
        "--quiet",
        "-q",
        action="store_const",
        const="CRITICAL",
        dest="log_level",
        help="Записывает в файлы и консоль только данные об ошибках",
    )
    log_level_group.add_argument(
        "--verbose",
        "-v",
        action="store_const",
        const="DEBUG",
        dest="log_level",
        help="Записывает в файлы и консоль расширенную информацию о процессе стратегии",
    )
    log_level_group.add_argument(
        "--silent",
        "-s",
        action="store_true",
        help="Предотвращает запись в файлы и консоль",
    )

    parser.add_argument(
        "--without-logs",
        "-w",
        action="store_true",
        help="Предотвращает запись логов в файлы. Не влияет на вывод логов в консоль",
    )

    parser.set_defaults(log_level="INFO")

    return parser


def setup_argsparser() -> argparse.ArgumentParser:
    """Конфигурация парсера аргументов консольной строки"""

    parser = argparse.ArgumentParser(
        description="Скрипт для обработки данных по квартирам застройщика ТДСК",
        parents=[create_global_parser()],
        add_help=False,
    )

    subparsers = parser.add_subparsers(
        title="commands",
        dest="command",
        required=True,
        help="Запуск выбранного сценария работы",
    )

    strategy_parser = subparsers.add_parser(
        "strategy",
        help="Запуск выбранной стратегии",
        parents=[create_global_parser()],
        add_help=False,
    )
    strategy_parser.add_argument(
        "strategy_",
        choices=config.STRATEGY_LIST,
        help="Запуск выбранной стратегии",
    )

    cleaner_parser = subparsers.add_parser(  # noqa F841
        "clean",
        help="Очищает папку логов",
        parents=[create_global_parser()],
        add_help=False,
    )

    return parser
