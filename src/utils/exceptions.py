class DependencyError(Exception):
    """Исключение, вызыванное отсутствием необходимой зависимости в словаре зависимостей"""

    def __init__(self, message: str = "Отсутствует необходимая зависимость в словаре зависимостей",):
        self.message = message
        super().__init__(self.message)


class StrategyError(Exception):
    """Исключение, вызыванное отсутствием необходимой стратегии в словаре стратегий"""

    def __init__(self, message: str = "Отсутствует необходимая стратегия в словаре стратегий"):
        self.message = message
        super().__init__(self.message)
