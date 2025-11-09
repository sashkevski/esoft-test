import pandas as pd

from src.processing.feature_engineering import FeaturesBuilder
from src.processing.preprocessor import DataPreprocessor


class TestDataPreprocessor:
    def test_prepare_old_data(self, sample_raw_data):
        preprocessor = DataPreprocessor()

        result = preprocessor.prepare_data(sample_raw_data)

        assert result is not None
        assert not result["gp"].isna().any()
        assert pd.api.types.is_numeric_dtype(result["area"])
        assert pd.api.types.is_numeric_dtype(result["price"])
        assert pd.api.types.is_datetime64_any_dtype(result["published_at"])
        assert pd.api.types.is_datetime64_any_dtype(result["actualized_at"])

    def test_prepare_parsed_data(self, sample_parsed_data):
        preprocessor = DataPreprocessor()

        result = preprocessor.prepare_data(sample_parsed_data)

        assert result is not None
        assert not result["gp"].isna().any()
        assert pd.api.types.is_numeric_dtype(result["area"])
        assert pd.api.types.is_numeric_dtype(result["price"])

    def test_extract_gp_from_address(self):
        preprocessor = DataPreprocessor()

        address_with_gp = "ул. Петра Ершова, д. 9, ГП-7.4"
        result = preprocessor._extract_gp_from_address(address_with_gp)
        assert result == "ГП-7.4"

        address_with_house = "ул. Монтажников, д. 40, подъезд 2"
        result = preprocessor._extract_gp_from_address(address_with_house)
        assert result == "Дом 40"

        address_without = "просто адрес"
        result = preprocessor._extract_gp_from_address(address_without)
        assert result is None


class TestFeaturesBuilder:
    def test_create_date_range(self):
        builder = FeaturesBuilder()

        result = builder.create_date_range("2023-07-01", "2023-07-05")

        assert len(result) == 5
        assert result["date"].min().strftime("%Y-%m-%d") == "2023-07-01"
        assert result["date"].max().strftime("%Y-%m-%d") == "2023-07-05"

    def test_create_monthly_activity_features(self, sample_raw_data):
        builder = FeaturesBuilder()

        df = sample_raw_data.copy()
        df["actualized_at"] = pd.to_datetime(df["actualized_at"])
        df["room_count"] = df["room_count"].astype(str)

        result = builder.create_monthly_activity_features(df)

        assert result is not None
        assert "1-комн." in result.columns

    def test_create_room_comparison_features(
        self, sample_raw_data, sample_parsed_data
    ):
        builder = FeaturesBuilder()

        result = builder.create_room_comparison_features(
            sample_raw_data, sample_parsed_data
        )

        assert "room_type" in result.columns
        assert "old_count" in result.columns
        assert "new_count" in result.columns
        assert len(result) > 0

    def test_create_area_comparison_features(
        self, sample_raw_data, sample_parsed_data
    ):
        builder = FeaturesBuilder()

        result = builder.create_area_comparison_features(
            sample_raw_data, sample_parsed_data
        )

        assert "area_range" in result.columns
        assert "old_count" in result.columns
        assert "new_count" in result.columns

    def test_create_price_comparison_features(
        self, sample_raw_data, sample_parsed_data
    ):
        builder = FeaturesBuilder()

        result = builder.create_price_comparison_features(
            sample_raw_data, sample_parsed_data
        )

        assert "price_range" in result.columns
        assert "old_count" in result.columns
        assert "new_count" in result.columns
