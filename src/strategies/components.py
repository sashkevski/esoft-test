import logging
from pathlib import Path

import pandas as pd

from config import config
from src.adapters.csv_repository import CSVRepository
from src.adapters.png_repository import PNGRepository
from src.aggregation.aggregator import DataAggregator
from src.parsing.parser import TDSKParser
from src.processing.feature_engineering import FeaturesBuilder
from src.processing.preprocessor import DataPreprocessor
from src.visualization.plots import PlotBuilder

logger = logging.getLogger(__name__)


def load_old_data(csv_repository: CSVRepository, file_path: str | Path) -> pd.DataFrame:
    """Компонент загрузки старых данных"""

    return csv_repository.load(file_path=file_path, separator=config.SEPARATOR)


def prepare_data(
    raw_data: pd.DataFrame,
    preprocessor: DataPreprocessor,
    csv_repository: CSVRepository,
    save_args: config.SAVE_ARGS,
) -> pd.DataFrame:
    """Компонент обработки старых данных"""

    logger.info("Обработка старых данных")

    prepared_old_data = preprocessor.prepare_data(df=raw_data)

    csv_repository.save(
        df=prepared_old_data,
        save_path=save_args.save_path,
        name=save_args.file_name,
        save_date=save_args.save_date,
    )

    return prepared_old_data


def prepare_data_without_saving(raw_data: pd.DataFrame, preprocessor: DataPreprocessor) -> pd.DataFrame:
    """Компонент обработки старых данных без сохранения в файл"""

    logger.info("Обработка старых данных")

    prepared_old_data = preprocessor.prepare_data(df=raw_data)

    return prepared_old_data


def create_pivot_table(
    prepared_old_data: pd.DataFrame,
    aggregator: DataAggregator,
    features_builder: FeaturesBuilder,
    csv_repository: CSVRepository,
    save_args: config.SAVE_ARGS,
) -> None:
    """Компонент создания сводной таблицы"""

    logger.info("Создание сводной таблицы")

    dates_df = features_builder.create_date_range(start_date=config.START_DATE, end_date=config.END_DATE)
    pivot = aggregator.create_active_objects_pivot(df=prepared_old_data, dates_df=dates_df)

    csv_repository.save(
        df=pivot,
        save_path=save_args.save_path,
        name=save_args.file_name,
        save_date=save_args.save_date,
    )


def create_monthly_plot(
    prepared_old_data: pd.DataFrame,
    features_builder: FeaturesBuilder,
    plot_builder: PlotBuilder,
    png_repository: PNGRepository,
    save_args: config.SAVE_ARGS,
) -> None:
    """Компонент создания графика активных объектов в разрезе комнатности"""

    logger.info("Создание таблицы признаков для построения графика")

    monthly_active_features = features_builder.create_monthly_activity_features(df=prepared_old_data)

    logger.info("Создание графика месячного количества активных объектов в разрезе комнатности")

    monthly_plot = plot_builder.plot_monthly_activity(features_df=monthly_active_features)

    png_repository.save(
        fig=monthly_plot,
        save_path=save_args.save_path,
        name=save_args.file_name,
        save_date=save_args.save_date,
    )


def parsing_tdsk(
    parser: TDSKParser,
    preprocessor: DataPreprocessor,
    csv_repository: CSVRepository,
    save_args: config.SAVE_ARGS,
) -> pd.DataFrame:
    """Компонент парсинга и обработки данных с сайта ТДСК"""

    logger.info("Парсинг сайта застройщика ТДСК")

    parsed_data = parser.parse_apartments()

    logger.info("Обработка данных после парсинга")

    prepared_parsed_data = preprocessor.prepare_data(df=parsed_data)
    csv_repository.save(
        df=prepared_parsed_data,
        save_path=save_args.save_path,
        name=save_args.file_name,
        save_date=save_args.save_date,
    )

    return prepared_parsed_data


def merge_datasets(
    prepared_old_data: pd.DataFrame,
    prepared_parsed_data: pd.DataFrame,
    aggregator: DataAggregator,
    csv_repository: CSVRepository,
    save_args: config.SAVE_ARGS,
) -> None:
    """Компонент сцепки новых и старых таблиц"""

    logger.info("Обогащение старых данных")

    merged_data = aggregator.saturate_old_data(old_data=prepared_old_data, new_data=prepared_parsed_data)
    csv_repository.save(
        df=merged_data,
        save_path=save_args.save_path,
        name=save_args.file_name,
        save_date=save_args.save_date,
    )


def create_room_comparison_plot(
    prepared_old_data: pd.DataFrame,
    prepared_parsed_data: pd.DataFrame,
    features_builder: FeaturesBuilder,
    plot_builder: PlotBuilder,
    png_repository: PNGRepository,
    save_args: config.SAVE_ARGS,
) -> None:
    """Компонент создания графика сравнение количества квартир по комнатности"""

    logger.info("Создание графика для сравнение количества квартир по комнатности между старой и новой выборкой")

    room_comparison_features = features_builder.create_room_comparison_features(
        old_data=prepared_old_data,
        new_data=prepared_parsed_data,
        )

    room_comparison_plot = plot_builder.plot_room_comparison(features_df=room_comparison_features)

    png_repository.save(
        fig=room_comparison_plot,
        save_path=save_args.save_path,
        name=save_args.file_name,
        save_date=save_args.save_date,
    )


def create_area_comparison_plot(
    prepared_old_data: pd.DataFrame,
    prepared_parsed_data: pd.DataFrame,
    features_builder: FeaturesBuilder,
    plot_builder: PlotBuilder,
    png_repository: PNGRepository,
    save_args: config.SAVE_ARGS,
) -> None:
    """Компонент создания графика сравнение количества квартир по площади"""

    logger.info("Создание графика для сравнение количества квартир по площади между старой и новой выборкой")

    area_comparison_features = features_builder.create_area_comparison_features(
        old_data=prepared_old_data,
        new_data=prepared_parsed_data,
        )

    area_comparison_plot = plot_builder.plot_area_comparison(features_df=area_comparison_features)
    png_repository.save(
        fig=area_comparison_plot,
        save_path=save_args.save_path,
        name=save_args.file_name,
        save_date=save_args.save_date,
    )


def create_price_comparison_plot(
    prepared_old_data: pd.DataFrame,
    prepared_parsed_data: pd.DataFrame,
    features_builder: FeaturesBuilder,
    plot_builder: PlotBuilder,
    png_repository: PNGRepository,
    save_args: config.SAVE_ARGS,
) -> None:
    """Компонент создания графика сравнение количества квартир по цене"""

    logger.info(
        "Создание графика для сравнение количества квартир по цене между старой и новой выборкой"
    )

    price_comparison_features = (
        features_builder.create_price_comparison_features(
            old_data=prepared_old_data,
            new_data=prepared_parsed_data,
        )
    )

    price_comparison_plot = plot_builder.plot_price_comparison(features_df=price_comparison_features)
    png_repository.save(
        fig=price_comparison_plot,
        save_path=save_args.save_path,
        name=save_args.file_name,
        save_date=save_args.save_date,
    )
