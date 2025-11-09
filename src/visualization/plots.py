import logging

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure

from src.utils.decorators import exceptions_handler

logger = logging.getLogger(__name__)


class PlotBuilder:
    @staticmethod
    def _plot_comparison_bars(
        features_df: pd.DataFrame,
        x_col: str,
        old_col: str,
        new_col: str,
        title: str,
        x_label: str,
        y_label: str,
    ) -> Figure:
        """Вспомогательный метод для построения сравнительных графиков"""

        fig, ax = plt.subplots(figsize=(12, 6))

        points = range(len(features_df))
        width = 0.35

        ax.bar([i - width / 2 for i in points], features_df[old_col], width, label="Старая выборка", alpha=0.7, )
        ax.bar([i + width / 2 for i in points], features_df[new_col], width, label="Новая выборка", alpha=0.7, )

        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)
        ax.set_xticks(points)
        ax.set_xticklabels(features_df[x_col], rotation=45)
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        return fig

    @staticmethod
    @exceptions_handler(logger=logger)
    def plot_monthly_activity(features_df: pd.DataFrame) -> Figure:
        """Создаёт график месячного количества активных объектов в разрезе комнатности"""

        fig, ax = plt.subplots(figsize=(12, 8))

        features_df.plot(kind="line", ax=ax, marker="o")
        ax.set_title("Месячное количество активных объектов по комнатности")
        ax.set_xlabel("Месяц")
        ax.set_ylabel("Количество объектов")
        ax.legend(title="Комнатность")
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()

        logger.debug("График месячного количества активных объектов в разрезе комнатности")

        return fig

    @exceptions_handler(logger=logger)
    def plot_room_comparison(self, features_df: pd.DataFrame) -> Figure:
        """Создаёт график сравнения комнатности между выборками"""

        fig = self._plot_comparison_bars(
            features_df,
            "room_type",
            "old_count",
            "new_count",
            "Сравнение комнатности между выборками",
            "Количество комнат",
            "Количество объектов",
        )

        logger.debug("График сравнения комнатности между выборками успешно создан")

        return fig

    @exceptions_handler(logger=logger)
    def plot_area_comparison(self, features_df: pd.DataFrame) -> Figure:
        """Создаёт график сранения распределения площадей между выборками"""

        fig = self._plot_comparison_bars(
            features_df,
            "area_range",
            "old_count",
            "new_count",
            "Сравнение распределения площадей между выборками", "Диапазон площади (м²)",
            "Количество объектов",
        )

        logger.debug("График сранения распределения площадей между выборками успешно создан")

        return fig

    @exceptions_handler(logger=logger)
    def plot_price_comparison(self, features_df: pd.DataFrame) -> Figure:
        """Создаёт график сранения распределения цен между выборками"""

        fig = self._plot_comparison_bars(
            features_df,
            "price_range",
            "old_count",
            "new_count",
            "Сравнение распределения цен между выборками",
            "Диапазон цены (млн руб)",
            "Количество объектов",
        )

        logger.debug("График сранения распределения цен между выборками успешно создан")

        return fig
