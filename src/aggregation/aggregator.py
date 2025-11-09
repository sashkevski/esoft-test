import logging

import pandas as pd

from src.utils.decorators import exceptions_handler

logger = logging.getLogger(__name__)


class DataAggregator:
    @staticmethod
    @exceptions_handler(logger=logger)
    def create_active_objects_pivot(df: pd.DataFrame, dates_df: pd.DataFrame) -> pd.DataFrame:
        """Создаёт сводную таблицу по актуальным квартирам"""

        df = df.assign()

        cross_table = pd.merge(dates_df, df[["gp", "actualized_at"]], how="cross")

        filtered_df = cross_table[
            (cross_table["actualized_at"].dt.month == cross_table["date"].dt.month)
            & (cross_table["actualized_at"].dt.day == cross_table["date"].dt.day)
        ]

        pivot = (filtered_df.groupby(["date", "gp"]).size().reset_index(name="actual_count"))

        pivot["date"] = pivot["date"].dt.strftime("%d.%m.%Y")
        pivot = pivot.rename(
            columns={
                "date": "Дата",
                "gp": "Корпус",
                "actual_count": "Кол-во активных квартир",
            }
        )

        return pivot

    @staticmethod
    @exceptions_handler(logger=logger)
    def saturate_old_data(old_data: pd.DataFrame, new_data: pd.DataFrame) -> pd.DataFrame:
        """Объединяет старые и новые данные, возвращает объединённую версию"""

        first = old_data.assign()
        second = new_data.assign()

        actualized_map = second.set_index("advert_id")["actualized_at"].to_dict()

        mask = first["advert_id"].isin(actualized_map)
        first.loc[mask, "actualized_at"] = first.loc[mask, "advert_id"].map(actualized_map)

        existing_ids = set(first["advert_id"])
        new_records = second[~second["advert_id"].isin(existing_ids)]

        merged = pd.concat([first, new_records], ignore_index=True)

        logger.debug("Таблицы успешно объеденены")

        return merged
