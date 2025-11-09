from src.adapters.csv_repository import CSVRepository
from src.adapters.png_repository import PNGRepository
from src.aggregation.aggregator import DataAggregator
from src.parsing.parser import TDSKParser
from src.processing.feature_engineering import FeaturesBuilder
from src.processing.preprocessor import DataPreprocessor
from src.visualization.plots import PlotBuilder
from src.strategies.strategies import MainStrategy, ParseStrategy

DEPENDENCY_MAP = {
    "aggregator": DataAggregator,
    "tdsk_parser": TDSKParser,
    "features_builder": FeaturesBuilder,
    "preprocessor": DataPreprocessor,
    "plot_builder": PlotBuilder,
    "csv_repository": CSVRepository,
    "png_repository": PNGRepository,
}

STRATEGY_MAP = {
    "main": MainStrategy,
    "parse": ParseStrategy,
}
