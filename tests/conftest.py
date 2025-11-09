import matplotlib
import pytest
import pandas as pd
import tempfile
from pathlib import Path
from datetime import datetime, timezone
import uuid

matplotlib.use("Agg")

@pytest.fixture
def sample_raw_data():
    """Фикстура с сырыми данными"""

    data = {
        "id": ["051a54b2-3ba7-4ee2-854d-83ecf42a4d24"],
        "advert_id": [320298],
        "domain": ["t-dsk.ru"],
        "developer": ["ТДСК"],
        "address": ["ул. Монтажников, д. 40, подъезд 2, квартира №98"],
        "gp": [None],
        "description": [
            "1-комнатная квартира на ул. Монтажников, дом 40 2 подъезд"
        ],
        "entrance_number": [2],
        "floor": [4],
        "area": [39.4],
        "room_count": [1],
        "flat_number": [98],
        "price": [4250000],
        "published_at": ["2023-06-01 05:39:34.605000+00:00"],
        "actualized_at": ["2023-08-01 00:04:42.827000+00:00"],
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_parsed_data():
    """Фикстура с обработанными спарсенными данными"""

    data = {
        "id": [str(uuid.uuid4())],
        "advert_id": [330489],
        "domain": ["t-dsk.ru"],
        "developer": ["ТДСК"],
        "address": ["ул. Петра Ершова, д. 9, ГП-7.4"],
        "gp": ["ГП-7.4"],
        "description": ["1-комнатная квартира ул. Петра Ершова, д. 9, ГП-7.4"],
        "entrance_number": [5],
        "floor": [14],
        "area": [41.1],
        "room_count": [1],
        "flat_number": [275],
        "price": [4150000],
        "published_at": [datetime.now(timezone.utc)],
        "actualized_at": [datetime.now(timezone.utc)],
    }
    return pd.DataFrame(data)


@pytest.fixture
def temp_dir():
    """Временная директория для тестов"""

    with tempfile.TemporaryDirectory() as dir:
        yield Path(dir)
