from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from .vk_api_error import VKError

if TYPE_CHECKING:
    from collections.abc import Iterator

    from vk_cli.models.vk_object import VKobject

    from .vk_request import VKRequest


class VKEmptyResponseError(Exception):
    pass


class VKResponse:
    """
    Presenting answer from API
    """

    def __init__(self, request: VKRequest, raw_data: dict) -> None:
        self.request = request
        self.raw_data = raw_data

        self._items = []
        self.error = None
        self.date = datetime.datetime.now()

        self._parse()

    def _parse(self) -> None:
        if isinstance(self.raw_data, dict):
            try:
                self._items = self.raw_data['items']
            except KeyError:  # single item
                self._items = [self.raw_data]

        elif isinstance(self.raw_data, list):
            self._items = self.raw_data

        elif isinstance(self.raw_data, VKError):
            self.error = self.raw_data

    def get_model_single(self) -> VKobject:
        return self.create_model_instance(self.single)

    def model_generator(self) -> Iterator[VKobject]:
        for data in self._items:
            try:
                yield self.create_model_instance(data)
            except StopIteration:
                return

    def ids_generator(self) -> Iterator[int]:
        for id_item in self._items:
            if not isinstance(id_item, int):
                return
            yield id_item

    def create_model_instance(self, data: dict) -> VKobject:
        """
        Создание экземпляра связанной модели на основе порции данных из полученного ответа
        """
        if not isinstance(data, dict):
            raise StopIteration

        return self.request.binded_model.from_data(vk=self.request._vk, data=data)

    @property
    def array(self) -> list[VKobject]:
        return self._items

    @property
    def single(self) -> dict:
        """
        Первый элемент в наборе данных
        """
        if not self._items:
            raise VKEmptyResponseError

        return self._items[0]

    @property
    def total(self) -> int:
        """
        Общее количество объектов в базовом запросе, если применимо
        """
        try:
            return self.raw_data.get('count') or self.count
        except AttributeError:
            return self.count

    @property
    def count(self) -> int:
        """
        Количество объектов в текущем подзапросе
        """
        return len(self._items)

    @property
    def is_number(self) -> bool:
        """
        Результат запроса - единичное число
        """
        return isinstance(self.raw_data, int)

    @property
    def get_number(self):
        if self.is_number:
            return self.raw_data
        return None
