import logging
import re

import pandas as pd

from config import config
from src.utils.decorators import exceptions_handler

logger = logging.getLogger(__name__)


class DataPreprocessor:
    @staticmethod
    def _extract_gp_from_address(address: str) -> str | None:
        """Извлекает номер корпуса из адреса, в инома случае - заполлняет номером дома"""

        gp_match = re.search(r"ГП-\d+(?:\.\d+)?", address)
        if gp_match:
            return gp_match.group()

        house_number_match = re.search(r"д\.?\s*(\d+[а-я]?)", address)
        if house_number_match:
            return f"Дом {house_number_match.group(1)}"

        return None

    @staticmethod
    def _cast_dates(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
        """Преобразование дат в формат datetime"""

        for column in columns:
            df[column] = pd.to_datetime(df[column], format="mixed", utc=True)

        return df

    @staticmethod
    def _cast_to_numeric(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
        """Преобразует значение колонки в числовой формат"""

        for column in columns:
            df[column] = pd.to_numeric(df[column])

        return df

    def _cast_columns(
        self,
        df: pd.DataFrame,
        numeric_columns: list[str],
        dates_columns: list[str],
    ) -> pd.DataFrame:
        """Вспомогательная функция для преобразования значений колонок для дат и чисел"""

        df = self._cast_dates(df, dates_columns)
        df = self._cast_to_numeric(df, numeric_columns)

        return df

    @exceptions_handler(logger=logger)
    def prepare_data(self, df: pd.DataFrame) -> pd.DataFrame | None:
        """Обрабатывает таблицу, заполняя пустые поля и приводит типы"""

        mask = df["gp"].isna()
        df.loc[mask, "gp"] = df[mask]["address"].map(self._extract_gp_from_address)

        df = self._cast_columns(df=df, numeric_columns=config.NUMERIC_COLUMNS, dates_columns=config.DATES_COLUMNS)

        logger.debug("Успешная нормализация таблицы")

        return df
