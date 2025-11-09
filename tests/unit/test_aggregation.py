import pandas as pd

from src.aggregation.aggregator import DataAggregator


class TestDataAggregator:
    def test_create_active_objects_pivot(self, sample_raw_data):
        aggregator = DataAggregator()

        df = sample_raw_data.copy()
        df["actualized_at"] = pd.to_datetime(df["actualized_at"])
        df["gp"] = "ГП-1"

        dates_df = pd.DataFrame(
            {"date": pd.date_range("2023-08-01", "2023-08-05", tz="UTC")}
        )

        result = aggregator.create_active_objects_pivot(df, dates_df)

        assert "Дата" in result.columns
        assert "Корпус" in result.columns
        assert "Кол-во активных квартир" in result.columns

    def test_saturate_old_data(self, sample_raw_data, sample_parsed_data):
        aggregator = DataAggregator()

        result = aggregator.saturate_old_data(
            sample_raw_data, sample_parsed_data
        )

        assert len(result) >= len(sample_raw_data)
        assert "advert_id" in result.columns
        assert "actualized_at" in result.columns

        advert_id = "330489"
        if advert_id in sample_raw_data["advert_id"].values:
            updated_row = result[result["advert_id"] == advert_id]
            assert not updated_row.empty
