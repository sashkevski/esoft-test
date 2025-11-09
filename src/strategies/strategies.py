import abc
import logging

from config import config
from src.strategies.components import (
    load_old_data,
    create_price_comparison_plot,
    create_room_comparison_plot,
    create_monthly_plot,
    create_area_comparison_plot,
    create_pivot_table,
    prepare_data,
    parsing_tdsk,
    merge_datasets,
)
from src.utils.decorators import strategy_timer
from src.utils.exceptions import StrategyError

logger = logging.getLogger(__name__)


class Strategy(abc.ABC):
    @abc.abstractmethod
    def execute(self) -> None:
        raise NotImplementedError


class MainStrategy(Strategy):
    """Основная стратегия выполнения программы"""

    def __init__(self):
        from src.utils.dependency import setup_dependencies

        self.dependencies = setup_dependencies(
            [
                "aggregator",
                "tdsk_parser",
                "features_builder",
                "preprocessor",
                "plot_builder",
                "csv_repository",
                "png_repository",
            ]
        )

    @strategy_timer
    def execute(self) -> None:
        raw = load_old_data(
            csv_repository=self.dependencies.csv_repository,
            file_path=config.RAW_DATA_PATH,
        )

        prepared_old_data = prepare_data(
            raw_data=raw,
            preprocessor=self.dependencies.preprocessor,
            csv_repository=self.dependencies.csv_repository,
            save_args=config.SAVE_ARGS(config.PREPARED_DATA_PATH, "prepared_data", False),
        )

        create_pivot_table(
            prepared_old_data=prepared_old_data,
            aggregator=self.dependencies.aggregator,
            features_builder=self.dependencies.features_builder,
            csv_repository=self.dependencies.csv_repository,
            save_args=config.SAVE_ARGS(config.OUTPUT_TABLES, "pivot_table", False),
        )

        create_monthly_plot(
            prepared_old_data=prepared_old_data,
            features_builder=self.dependencies.features_builder,
            plot_builder=self.dependencies.plot_builder,
            png_repository=self.dependencies.png_repository,
            save_args=config.SAVE_ARGS(config.OUTPUT_PLOTS, "plot_monthly_activity", False),
        )

        prepared_parsed_data = parsing_tdsk(
            parser=self.dependencies.tdsk_parser,
            preprocessor=self.dependencies.preprocessor,
            csv_repository=self.dependencies.csv_repository,
            save_args=config.SAVE_ARGS(config.PARSED_DATA_PATH, "parsed_data", True),
        )

        merge_datasets(
            prepared_old_data=prepared_old_data,
            prepared_parsed_data=prepared_parsed_data,
            aggregator=self.dependencies.aggregator,
            csv_repository=self.dependencies.csv_repository,
            save_args=config.SAVE_ARGS(config.MERGED_DATA_PATH, "merged_data", True),
        )

        create_room_comparison_plot(
            prepared_old_data=prepared_old_data,
            prepared_parsed_data=prepared_parsed_data,
            features_builder=self.dependencies.features_builder,
            plot_builder=self.dependencies.plot_builder,
            png_repository=self.dependencies.png_repository,
            save_args=config.SAVE_ARGS(config.OUTPUT_PLOTS, "room_comparison_plot", True),
        )

        create_area_comparison_plot(
            prepared_old_data=prepared_old_data,
            prepared_parsed_data=prepared_parsed_data,
            features_builder=self.dependencies.features_builder,
            plot_builder=self.dependencies.plot_builder,
            png_repository=self.dependencies.png_repository,
            save_args=config.SAVE_ARGS(config.OUTPUT_PLOTS, "area_comparison_plot", True),
        )

        create_price_comparison_plot(
            prepared_old_data=prepared_old_data,
            prepared_parsed_data=prepared_parsed_data,
            features_builder=self.dependencies.features_builder,
            plot_builder=self.dependencies.plot_builder,
            png_repository=self.dependencies.png_repository,
            save_args=config.SAVE_ARGS(config.OUTPUT_PLOTS, "price_comparison_plot", True),
        )


class ParseStrategy(Strategy):
    """Стратегия парсинга"""

    def __init__(self):
        from src.utils.dependency import setup_dependencies

        self.dependencies = setup_dependencies(["tdsk_parser", "preprocessor", "csv_repository"])

    @strategy_timer
    def execute(self) -> None:
        parsing_tdsk(
            parser=self.dependencies.tdsk_parser,
            preprocessor=self.dependencies.preprocessor,
            csv_repository=self.dependencies.csv_repository,
            save_args=config.SAVE_ARGS(config.PARSED_DATA_PATH, "tdsk", True),
        )


class Context:
    """Управляет выполнением стратегии"""

    def __init__(self, strategy: str):
        self._strategy = self._setup_strategy(strategy)

    @staticmethod
    def _setup_strategy(strategy: str) -> Strategy:
        from src.utils.constants import STRATEGY_MAP

        try:
            return STRATEGY_MAP[strategy]()

        except KeyError as e:
            raise StrategyError from e

    def start_strategy(self) -> None:
        self._strategy.execute()

    def set_strategy(self, strategy: str) -> None:
        self._strategy = self._setup_strategy(strategy=strategy)
