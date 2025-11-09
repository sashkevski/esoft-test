import datetime
import logging
from pathlib import Path

from matplotlib.figure import Figure

logger = logging.getLogger(__name__)


class PNGRepository:
    @staticmethod
    def save(
        fig: Figure,
        save_path: str | Path,
        name: str | None = None,
        save_date: bool = False,
    ) -> None:
        """Сохранение графиков"""

        if name and save_date:
            file_name = f"{name}_{datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d_%H-%M-%S-%f')}.png"

        elif name and not save_date:
            file_name = f"{name}.png"

        else:
            file_name = f"{datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d_%H-%M-%S-%f')}.png"

        try:
            fig.savefig(
                f"{save_path}/{file_name}",
                dpi=300,
                bbox_inches="tight",
                facecolor="white",
                edgecolor="none",
            )
            logger.info(
                f"Файл сохранён в директории: {save_path} с названием {file_name}"
            )

        except Exception as e:
            logger.error(
                f"Ошибка при сохранении файла с название {file_name} в директории: {save_path} : {e}"
            )
            raise e
