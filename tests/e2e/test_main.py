from unittest.mock import patch, MagicMock
import argparse
import pytest

from main import main


@pytest.fixture
def mock_args():
    def _create_mock_args(command, **kwargs):
        mock_args = argparse.Namespace()
        mock_args.command = command
        mock_args.log_level = kwargs.get('log_level', 'INFO')
        mock_args.without_logs = kwargs.get('without_logs', False)
        mock_args.silent = kwargs.get('silent', False)

        if command == "strategy":
            mock_args.strategy_ = kwargs.get('strategy_', 'main')

        return mock_args

    return _create_mock_args


@pytest.fixture
def mock_dependencies():
    with patch("main.setup_logger") as mock_logger, \
        patch("main.setup_argsparser") as mock_arg_parser:
        mock_parser = MagicMock()
        mock_arg_parser.return_value = mock_parser

        yield {
            'mock_logger': mock_logger,
            'mock_arg_parser': mock_arg_parser,
            'mock_parser': mock_parser
        }


class TestMainE2E:

    def test_main_strategy_command(self, mock_args, mock_dependencies):
        test_args = mock_args("strategy", strategy_="main")
        mock_dependencies['mock_parser'].parse_args.return_value = test_args

        with patch("main.Context") as mock_context:
            mock_instance = MagicMock()
            mock_context.return_value = mock_instance
            main()

            mock_instance.start_strategy.assert_called_once()

    def test_main_clean_command(self, mock_args, mock_dependencies):
        test_args = mock_args("clean")
        mock_dependencies['mock_parser'].parse_args.return_value = test_args

        with patch("main.clear_folder") as mock_clean:
            main()

            mock_clean.assert_called_once()
