import matplotlib.pyplot as plt

from src.adapters.csv_repository import CSVRepository
from src.adapters.png_repository import PNGRepository


class TestCSVRepository:
    def test_save_and_load(self, temp_dir, sample_raw_data):
        repo = CSVRepository()
        save_path = temp_dir / "test_save"
        save_path.mkdir()

        repo.save(
            df=sample_raw_data,
            save_path=save_path,
            name="test_data",
            save_date=False,
        )

        saved_file = save_path / "test_data.csv"
        assert saved_file.exists()

        loaded_data = repo.load(
            file_path=save_path / "test_data", separator=","
        )

        assert loaded_data is not None
        assert len(loaded_data) == len(sample_raw_data)
        assert "advert_id" in loaded_data.columns

    def test_save_with_date(self, temp_dir, sample_raw_data):
        repo = CSVRepository()
        save_path = temp_dir / "test_save_date"
        save_path.mkdir()

        repo.save(
            df=sample_raw_data,
            save_path=save_path,
            name="test_data",
            save_date=True,
        )

        files = list(save_path.glob("test_data_*.csv"))
        assert len(files) == 1


class TestPNGRepository:
    def test_save_figure(self, temp_dir):
        repo = PNGRepository()
        save_path = temp_dir / "test_plots"
        save_path.mkdir(parents=True)

        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [1, 2, 3])

        repo.save(
            fig=fig, save_path=save_path, name="test_plot", save_date=False
        )

        saved_file = save_path / "test_plot.png"
        assert saved_file.exists()

        plt.close(fig)
