from unittest.mock import Mock, patch

import pytest

from src.parsing.argsparser import setup_argsparser, create_global_parser
from src.parsing.parser import TDSKParser


class TestArgParser:
    def test_create_global_parser(self):
        parser = create_global_parser()

        assert any(action.dest == "log_level" for action in parser._actions)
        assert any(action.dest == "silent" for action in parser._actions)
        assert any(action.dest == "without_logs" for action in parser._actions)

    def test_setup_argsparser(self):
        parser = setup_argsparser()

        subparser_actions = [
            action for action in parser._actions if hasattr(action, "choices")
        ]
        assert len(subparser_actions) > 0
        assert hasattr(subparser_actions[0], "choices")


class TestTDSKParser:
    @patch("src.parsing.parser.requests.Session")
    def test_parse_apartments_success(self, mock_session):
        mock_response = Mock()
        mock_response.text = """
        <html>
            <span class="search-result__count-value">10</span>
            <div class="search-result__list-item list-item">
                <a class="search-result__link" data-id="123" data-floor="5" data-rooms="2" data-number="101" data-price="5000000"></a>
                <div class="search-result__object-bottom">ул. Тестовая, д. 1</div>
                <div class="search-result__td square">45.5</div>
                <div class="search-result__object-top">2-комнатная квартира</div>
                <div class="search-result__td">Подъезд 1</div>
                <div class="search-result__td">Доп информация</div>
            </div>
        </html>
        """

        mock_session_instance = Mock()
        mock_session_instance.get.return_value = mock_response
        mock_session.return_value = mock_session_instance

        parser = TDSKParser()
        parser.session = mock_session_instance

        result = parser.parse_apartments()

        assert result is not None
        assert len(result) > 0
        assert "advert_id" in result.columns

    @patch("src.parsing.parser.requests.Session")
    def test_parse_apartments_no_count(self, mock_session):
        mock_response = Mock()
        mock_response.text = "<html></html>"

        mock_session_instance = Mock()
        mock_session_instance.get.return_value = mock_response
        mock_session.return_value = mock_session_instance

        parser = TDSKParser()
        parser.session = mock_session_instance

        with pytest.raises(ValueError) as exc_info:
            parser.parse_apartments()
            assert "неудалось" in str(exc_info)
