import pandas as pd
import matplotlib.pyplot as plt

from src.visualization.plots import PlotBuilder


class TestPlotBuilder:
    def test_plot_monthly_activity(self):
        builder = PlotBuilder()

        features_df = pd.DataFrame(
            {
                "1-комн.": [10, 15, 12],
                "2-комн.": [5, 8, 7],
                "3-комн.": [2, 3, 4],
            },
            index=pd.PeriodIndex(["2023-07", "2023-08", "2023-09"], freq="M"),
        )

        fig = builder.plot_monthly_activity(features_df)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_plot_room_comparison(self):
        builder = PlotBuilder()

        features_df = pd.DataFrame(
            {
                "room_type": ["1-комн.", "2-комн.", "3-комн."],
                "old_count": [10, 5, 2],
                "new_count": [12, 6, 3],
            }
        )

        fig = builder.plot_room_comparison(features_df)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_plot_area_comparison(self):
        builder = PlotBuilder()

        features_df = pd.DataFrame(
            {
                "area_range": ["20-30", "30-40", "40-50"],
                "old_count": [5, 8, 3],
                "new_count": [6, 9, 4],
            }
        )

        fig = builder.plot_area_comparison(features_df)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_plot_price_comparison(self):
        builder = PlotBuilder()

        features_df = pd.DataFrame(
            {
                "price_range": ["<4млн", "4-5млн", "5-6млн"],
                "old_count": [3, 7, 5],
                "new_count": [4, 8, 6],
            }
        )

        fig = builder.plot_price_comparison(features_df)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)
