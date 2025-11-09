from unittest.mock import Mock, patch

import pandas as pd

from src.strategies.components import (
    load_old_data,
    prepare_data,
    create_pivot_table,
    parsing_tdsk,
)


class TestComponentsIntegration:
    def test_load_old_data_integration(self, temp_dir, sample_raw_data):
        test_file = temp_dir / "raw_data.csv"
        sample_raw_data.to_csv(test_file, sep="\t", index=False)

        csv_repo_mock = Mock()
        csv_repo_mock.load.return_value = sample_raw_data

        result = load_old_data(
            csv_repository=csv_repo_mock, file_path=temp_dir / "raw_data"
        )

        assert result is not None
        csv_repo_mock.load.assert_called_once()

    def test_prepare_old_data_integration(self, sample_raw_data):
        preprocessor_mock = Mock()
        preprocessor_mock.prepare_data.return_value = sample_raw_data

        csv_repo_mock = Mock()

        result = prepare_data(
            raw_data=sample_raw_data,
            preprocessor=preprocessor_mock,
            csv_repository=csv_repo_mock,
            save_args=Mock(
                save_path="/test", file_name="test", save_date=False
            ),
        )

        assert result is not None
        preprocessor_mock.prepare_data.assert_called_once()
        csv_repo_mock.save.assert_called_once()

    @patch("src.strategies.components.config")
    def test_create_pivot_table_integration(
        self, mock_config, sample_raw_data
    ):
        mock_config.START_DATE = "2023-07-01"
        mock_config.END_DATE = "2023-12-31"

        aggregator_mock = Mock()
        aggregator_mock.create_active_objects_pivot.return_value = (
            pd.DataFrame()
        )

        features_builder_mock = Mock()
        features_builder_mock.create_date_range.return_value = pd.DataFrame()

        csv_repo_mock = Mock()

        create_pivot_table(
            prepared_old_data=sample_raw_data,
            aggregator=aggregator_mock,
            features_builder=features_builder_mock,
            csv_repository=csv_repo_mock,
            save_args=Mock(
                save_path="/test", file_name="test", save_date=False
            ),
        )

        features_builder_mock.create_date_range.assert_called_once()
        aggregator_mock.create_active_objects_pivot.assert_called_once()
        csv_repo_mock.save.assert_called_once()

    def test_parsing_tdsk_integration(self, sample_parsed_data):
        parser_mock = Mock()
        parser_mock.parse_apartments.return_value = sample_parsed_data

        preprocessor_mock = Mock()
        preprocessor_mock.prepare_parsed_data.return_value = sample_parsed_data

        csv_repo_mock = Mock()

        result = parsing_tdsk(
            parser=parser_mock,
            preprocessor=preprocessor_mock,
            csv_repository=csv_repo_mock,
            save_args=Mock(
                save_path="/test", file_name="test", save_date=False
            ),
        )

        assert result is not None
        parser_mock.parse_apartments.assert_called_once()
        preprocessor_mock.prepare_data.assert_called_once()
        csv_repo_mock.save.assert_called_once()
