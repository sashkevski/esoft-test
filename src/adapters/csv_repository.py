import datetime
import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


class CSVRepository:
    @staticmethod
    def load(
        file_path: str | Path, separator: str | None
    ) -> pd.DataFrame | None:
        """Загрузка данных"""

        logger.info("Загрузка данных")

        try:
            df = pd.read_csv(f"{file_path}.csv", sep=separator)
            return df

        except Exception as e:  # noqa
            logger.error(f"Ошибка при импорте CSV файла {file_path}.csv : {e}")
            raise e

    @staticmethod
    def save(
        df: pd.DataFrame,
        save_path: str | Path,
        name: str | None = None,
        save_date: bool = False,
    ) -> None:
        """Сохранение данных"""

        logger.info("Сохранение данных")

        if name and save_date:
            file_name = f"{name}_{datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d_%H-%M-%S-%f')}.csv"

        elif name and not save_date:
            file_name = f"{name}.csv"

        else:
            file_name = f"{datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d_%H-%M-%S-%f')}.csv"

        try:
            df.to_csv(f"{save_path}/{file_name}", index=False)
            logger.info(
                f"Файл сохранён в директории: {save_path} с названием {file_name}"
            )

        except Exception as e:
            logger.error(
                f"Ошибка при сохранении файла с название {file_name} в директории: {save_path} : {e}"
            )
            raise e
