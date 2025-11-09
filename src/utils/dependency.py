from collections import namedtuple

from src.utils.constants import DEPENDENCY_MAP
from src.utils.exceptions import DependencyError


def setup_dependencies(dependencies: list[str]):
    """Создаёт необходимые зависимости"""

    try:
        dependencies_namedtuple = namedtuple("dependencies", dependencies)
        instances = [DEPENDENCY_MAP[dep]() for dep in dependencies]
        return dependencies_namedtuple(*instances)

    except KeyError as e:
        raise DependencyError from e
