import pytest
from unittest.mock import Mock, patch
import logging

from src.utils.cleaner import clear_folder
from src.utils.dependency import setup_dependencies
from src.utils.exceptions import DependencyError, StrategyError
from src.utils.decorators import strategy_timer


class TestCleaner:
    def test_clear_folder(self, temp_dir):
        test_file1 = temp_dir / "test1.txt"
        test_file2 = temp_dir / "test2.txt"
        test_file1.write_text("test content")
        test_file2.write_text("test content")

        assert test_file1.exists()
        assert test_file2.exists()
        clear_folder(str(temp_dir))

        assert not test_file1.exists()
        assert not test_file2.exists()


class TestDependency:
    def test_setup_dependencies_success(self):
        with patch("src.utils.dependency.DEPENDENCY_MAP", {"test_dep": Mock}):
            dependencies = setup_dependencies(["test_dep"])
            assert hasattr(dependencies, "test_dep")
            assert isinstance(dependencies.test_dep, Mock)

    def test_setup_dependencies_failure(self):
        with patch("src.utils.dependency.DEPENDENCY_MAP", {}):
            with pytest.raises(DependencyError):
                setup_dependencies(["nonexistent_dep"])


class TestExceptions:
    def test_dependency_error_exception(self):
        with pytest.raises(DependencyError) as exc_info:
            raise DependencyError()
        assert "зависимость в словаре зависимостей" in str(exc_info.value)

    def test_strategy_error_exception(self):
        with pytest.raises(StrategyError) as exc_info:
            raise StrategyError()
        assert "стратегия в словаре стратегий" in str(exc_info.value)


class TestDecorators:
    def test_cls_timer(self, caplog):
        logging.basicConfig(level=logging.INFO)

        class TestClass:
            @strategy_timer
            def test_method(self):
                return "test_result"

        obj = TestClass()

        with caplog.at_level(logging.INFO):
            result = obj.test_method()

        assert result == "test_result"
        assert any(
            "Запуск стратегии" in record.message for record in caplog.records
        )
        assert any(
            "успешно выполнилась" in record.message
            for record in caplog.records
        )
