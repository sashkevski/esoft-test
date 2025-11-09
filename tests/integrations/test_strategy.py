import pytest
from unittest.mock import Mock, patch

from src.strategies.strategies import MainStrategy, ParseStrategy, Context
from src.utils.exceptions import StrategyError


class TestStrategiesIntegration:
    @patch("src.utils.dependency.setup_dependencies")
    def test_main_strategy_execute(self, mock_setup_deps):
        deps_mock = Mock()
        deps_mock.csv_repository = Mock()
        deps_mock.preprocessor = Mock()
        deps_mock.aggregator = Mock()
        deps_mock.features_builder = Mock()
        deps_mock.plot_builder = Mock()
        deps_mock.png_repository = Mock()
        deps_mock.tdsk_parser = Mock()

        deps_mock.csv_repository.load.return_value = Mock()
        deps_mock.preprocessor.prepare_data.return_value = Mock()
        deps_mock.tdsk_parser.parse_apartments.return_value = Mock()

        mock_setup_deps.return_value = deps_mock

        with patch("src.strategies.strategies.config") as mock_config:
            mock_config.RAW_DATA_PATH = "/test/path"
            mock_config.PREPARED_DATA_PATH = "/test/path"
            mock_config.OUTPUT_TABLES = "/test/path"
            mock_config.OUTPUT_PLOTS = "/test/path"
            mock_config.PARSED_DATA_PATH = "/test/path"
            mock_config.MERGED_DATA_PATH = "/test/path"
            mock_config.SAVE_ARGS = Mock(
                return_value=Mock(
                    save_path="/test/path", file_name="test", save_date=False
                )
            )

            strategy = MainStrategy()
            strategy.execute()

            assert deps_mock.csv_repository.load.called
            assert deps_mock.preprocessor.prepare_data.called

    @patch("src.utils.dependency.setup_dependencies")
    def test_parse_strategy_execute(self, mock_setup_deps):
        deps_mock = Mock()
        deps_mock.tdsk_parser = Mock()
        deps_mock.preprocessor = Mock()
        deps_mock.csv_repository = Mock()

        deps_mock.tdsk_parser.parse_apartments.return_value = Mock()

        mock_setup_deps.return_value = deps_mock

        with patch("src.strategies.strategies.config") as mock_config:
            mock_config.PARSED_DATA_PATH = "/test/path"
            mock_config.SAVE_ARGS = Mock(
                return_value=Mock(
                    save_path="/test/path", file_name="test", save_date=False
                )
            )

            strategy = ParseStrategy()
            strategy.execute()

            deps_mock.tdsk_parser.parse_apartments.assert_called_once()
            deps_mock.preprocessor.prepare_data.assert_called_once()

    def test_context_success(self):
        with patch("src.utils.constants.STRATEGY_MAP", {"main": MainStrategy}):
            context = Context("main")
            assert context._strategy is not None

    def test_context_failure(self):
        with patch("src.utils.constants.STRATEGY_MAP", {}):
            with pytest.raises(StrategyError):
                Context("nonexistent")

    def test_context_set_strategy(self):
        with patch(
            "src.utils.constants.STRATEGY_MAP", {"main": Mock, "parse": Mock}
        ):
            context = Context("main")
            context.set_strategy("parse")
            assert context._strategy is not None
