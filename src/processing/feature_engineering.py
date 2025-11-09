import logging
import warnings

import pandas as pd

from config import config
from src.utils.decorators import exceptions_handler

logger = logging.getLogger(__name__)


class FeaturesBuilder:
    @staticmethod
    def create_date_range(start_date: str, end_date: str) -> pd.DataFrame:
        """Создаёт диапазон дат"""

        date_range = pd.date_range(start_date, end_date, tz="UTC")
        dates_df = pd.DataFrame({"date": date_range})
        return dates_df

    @staticmethod
    @exceptions_handler(logger=logger)
    def create_monthly_activity_features(df: pd.DataFrame) -> pd.DataFrame:
        """Создаёт таблицу признаков для сравнения месячного количества активных объектов в разрезе комнатности"""

        df_copy = df.assign()
        features = pd.DataFrame()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            features["month"] = df_copy["actualized_at"].dt.to_period("M")

        features["room_count"] = df_copy["room_count"].astype(str) + "-комн."

        features = (features.groupby(["month", "room_count"]).size().reset_index(name="count"))

        features = features.pivot(index="month", columns="room_count", values="count").fillna(0)

        return features

    @staticmethod
    @exceptions_handler(logger=logger)
    def create_room_comparison_features(old_data: pd.DataFrame, new_data: pd.DataFrame) -> pd.DataFrame:
        """Создаёт таблицу признаков для сравнения комнатности по количеству квартир"""

        old_rooms = old_data["room_count"].value_counts().sort_index()
        new_rooms = new_data["room_count"].value_counts().sort_index()

        features = pd.DataFrame({"old_count": old_rooms, "new_count": new_rooms}).fillna(0)

        features_df = features.reset_index()
        features_df["room_type"] = features_df.index.map(lambda x: f"{int(x) + 1}-комн.")

        return features_df[["room_type", "old_count", "new_count"]]

    @staticmethod
    @exceptions_handler(logger=logger)
    def create_area_comparison_features(old_data: pd.DataFrame, new_data: pd.DataFrame) -> pd.DataFrame:
        """Создает таблицу признаков для сравнения площадей по количеству квартир"""

        bins = config.AREA_RANGES
        labels = config.AREA_LABELS

        old_areas = (pd.cut(old_data["area"], bins=bins, labels=labels, right=False).value_counts().sort_index())
        new_areas = (pd.cut(new_data["area"], bins=bins, labels=labels, right=False).value_counts().sort_index())

        features = pd.DataFrame({"old_count": old_areas, "new_count": new_areas}).fillna(0)

        features = features.reset_index()
        features.rename(columns={"area": "area_range"}, inplace=True)

        return features

    @staticmethod
    @exceptions_handler(logger=logger)
    def create_price_comparison_features(old_data: pd.DataFrame, new_data: pd.DataFrame) -> pd.DataFrame:
        """Создает фичи для сравнения цен по количеству квартир"""

        bins = config.PRICE_RANGES
        labels = config.PRICE_LABELS

        old_prices = (pd.cut(old_data["price"], bins=bins, labels=labels, right=False).value_counts().sort_index())
        new_prices = (pd.cut(new_data["price"], bins=bins, labels=labels, right=False).value_counts().sort_index())

        features = pd.DataFrame({"old_count": old_prices, "new_count": new_prices}).fillna(0)

        features = features.reset_index()
        features.rename(columns={"price": "price_range"}, inplace=True)

        return features
