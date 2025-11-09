import logging
import os
from collections import namedtuple
from datetime import datetime
from pathlib import Path


class Config:
    """Конфигурация приложения"""

    # Базовая директория расположения приложения
    BASE_DIR = Path(__file__).parent

    # Сепаратор для старой таблицы
    SEPARATOR = "\t"

    # Список стратегий
    STRATEGY_LIST = ["main", "parse"]

    # Аргументы функции сохранения
    SAVE_ARGS = namedtuple(
        "SAVE_ARGS", ["save_path", "file_name", "save_date"]
    )

    # Директории к данным
    RAW_DATA_PATH = (
        BASE_DIR
        / "data"
        / "raw"
        / "Экспозиция ТДСК с 01.07.2023 по 31.12.2023"
    )
    MERGED_DATA_PATH = BASE_DIR / "data" / "merged_data"
    PARSED_DATA_PATH = BASE_DIR / "data" / "parsed_data"
    PREPARED_DATA_PATH = BASE_DIR / "data" / "prepared_data"

    # Настройки парсера
    PARSER_URL = (
        "https://www.t-dsk.ru/buildings/search-apartments/?objects=all"
    )
    PARSER_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    # Колонки типов
    DATES_COLUMNS = ["published_at", "actualized_at"]
    NUMERIC_COLUMNS = [
        "advert_id",
        "entrance_number",
        "floor",
        "area",
        "room_count",
        "flat_number",
        "price",
    ]

    # Список колонок таблицы
    BASE_COLUMNS = [
        "id",
        "advert_id",
        "domain",
        "developer",
        "address",
        "gp",
        "description",
        "entrance_number",
        "floor",
        "area",
        "room_count",
        "flat_number",
        "price",
        "published_at",
        "actualized_at",
    ]

    # Диапазоны для анализа
    START_DATE = "2023-07-01"
    END_DATE = "2023-12-31"

    AREA_RANGES = [0, 20, 30, 40, 50, 60, 70, 80, 90, 100, float("inf")]
    AREA_LABELS = [
        "<20",
        "20-30",
        "30-40",
        "40-50",
        "50-60",
        "60-70",
        "70-80",
        "80-90",
        "90-100",
        ">100",
    ]

    PRICE_RANGES = [0, 4e6, 5e6, 6e6, 7e6, 8e6, float("inf")]
    PRICE_LABELS = ["<4млн", "4-5млн", "5-6млн", "6-7млн", "7-8млн", ">8млн"]

    # Директории для вывода
    OUTPUT_TABLES = BASE_DIR / "output" / "tables"
    OUTPUT_PLOTS = BASE_DIR / "output" / "plots"

    LOG_DIR = BASE_DIR / "logs"

    # Создёт необходимые директории
    os.makedirs(MERGED_DATA_PATH, exist_ok=True)
    os.makedirs(PARSED_DATA_PATH, exist_ok=True)
    os.makedirs(PREPARED_DATA_PATH, exist_ok=True)

    os.makedirs(f"{BASE_DIR}/output", exist_ok=True)
    os.makedirs(OUTPUT_TABLES, exist_ok=True)
    os.makedirs(OUTPUT_PLOTS, exist_ok=True)


config = Config()


def setup_logger(
    log_level: str = "INFO", without_logs: bool = False, silent: bool = False
) -> None:
    """Конфигурация логирования, создание директории для логов"""

    if silent:
        logging.getLogger().setLevel(logging.CRITICAL + 1)
        return

    os.makedirs(config.LOG_DIR, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if not without_logs:
        log_file = f"{config.LOG_DIR}/analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)
        logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    logger.addHandler(console_handler)
