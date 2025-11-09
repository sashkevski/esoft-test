import logging
import uuid
from datetime import timezone, datetime as dt

import pandas as pd
import requests
from bs4 import BeautifulSoup, ResultSet
from bs4.element import Tag

from config import config
from src.utils.decorators import exceptions_handler

logger = logging.getLogger(__name__)


class TDSKParser:
    def __init__(self):
        self.config = config
        self.base_url = self.config.PARSER_URL
        self.session = requests.Session()
        self.session.headers.update(self.config.PARSER_HEADERS)

    def _get_max_count(self) -> int:
        """Находит количество доступных квартир на сайте"""

        response = self.session.get(self.base_url)
        bs = BeautifulSoup(response.text, "html.parser")
        count = bs.find("span", class_="search-result__count-value")

        if count:
            return int(count.text)

        else:
            raise ValueError("Не удалось получить количество доступных квартир")

    def _get_apartments(self, page: int) -> ResultSet:
        """Парсит квартиры со страницы"""

        params = {"PAGEN_3": str(page)}
        response = self.session.get(self.base_url, params=params)
        bs = BeautifulSoup(response.text, "html.parser")

        apartments = bs.find_all("div",class_="search-result__list-item search-result__list-item--action list-item")

        apartments += bs.find_all("div", class_="search-result__list-item list-item")

        if apartments:
            return apartments

        else:
            raise ValueError("Не удалось получить квартиры со страницы сайта")

    def _process_apartments(
        self, apartments: ResultSet, df: pd.DataFrame
    ) -> pd.DataFrame:
        """Обрабатывает список квартир, заполняя таблицу квартир"""

        for apartment in apartments:
            data = self._parse_apartments_element(apartment=apartment)
            df.loc[len(df)] = data

        return df

    @staticmethod
    @exceptions_handler(logger=logger)
    def _parse_apartments_element(apartment: Tag) -> dict:
        """Обрабатывает одну квартиру, возвращая её данные"""

        data = apartment.find("a", class_="search-result__link")
        address = apartment.find("div", class_="search-result__object-bottom").text.strip()
        area = apartment.find("div", class_="search-result__td square").text.strip()
        description = apartment.find("div", class_="search-result__object-top").text.strip()
        entrance = apartment.find_all("div", class_="search-result__td")

        if all([data, area, description, entrance]):
            return {
                "id": uuid.uuid4(),
                "advert_id": data["data-id"].strip(),
                "domain": "t-dsk.ru",
                "developer": "ТДСК",
                "address": address,
                "gp": None,
                "description": description + " " + address,
                "entrance_number": entrance[1].text.strip(),  # подъезд
                "floor": data["data-floor"].strip(),  # этаж
                "area": area.replace(",", "."),  # площадь
                "room_count": data["data-rooms"],  # кол-во комнат
                "flat_number": data["data-number"].strip(),  # квартира
                "price": data["data-price"].replace(" ", ""),
                "published_at": dt.now(timezone.utc),
                "actualized_at": dt.now(timezone.utc),
            }

        else:
            raise ValueError("Не удалось заполучить данные квартиры")

    @exceptions_handler(logger=logger)
    def parse_apartments(self) -> pd.DataFrame | None:
        """Парсинг сайта застройщика ТДСК"""

        columns = self.config.BASE_COLUMNS
        df = pd.DataFrame(columns=columns)

        page = 1
        current_count = 0
        max_count = self._get_max_count()

        while True:
            apartments = self._get_apartments(page=page)

            current_count += len(apartments)

            if current_count > max_count or len(apartments) == 0:
                break

            self._process_apartments(apartments=apartments, df=df)

            page += 1

        return df
