import datetime

from .vk_api_error import VKError


class VKEmptyResponse(Exception):
    pass


class VKResponse:
    """
    Presenting answer from API
    """

    error = None

    def __init__(self, request, raw_data):
        self.request = request  # source request (VKRequest)
        self.raw_data = raw_data

        self._items = []
        self.date = datetime.datetime.now()

        self._parse()

    def _parse(self):
        if isinstance(self.raw_data, dict):
            try:
                self._items = self.raw_data['items']
            except KeyError:  # single item
                self._items = [self.raw_data]

        elif isinstance(self.raw_data, list):
            self._items = self.raw_data

        elif isinstance(self.raw_data, VKError):
            self.error = self.raw_data

    def get_model_single(self):
        return self.create_model_instance(self.single)

    def model_generator(self):
        for data in self._items:
            try:
                yield self.create_model_instance(data)
            except StopIteration:
                return

    def ids_generator(self):
        for id_item in self._items:
            if not isinstance(id_item, int):
                return
            yield id_item

    def create_model_instance(self, data):
        """
        Создание экземпляра связанной модели на основе порции данных из полученного ответа
        :param data:
        :return:
        """
        if not isinstance(data, dict):
            raise StopIteration

        return self.request.binded_model.from_data(data=data)

    @property
    def array(self):
        return self._items

    @property
    def single(self):
        """
        Первый элемент в наборе данных
        :return:
        """
        if not self._items:
            raise VKEmptyResponse

        return self._items[0]

    @property
    def total(self):
        """
        Общее количество объектов в базовом запросе, если применимо
        :return:
        """
        try:
            return self.raw_data.get('count') or self.count
        except AttributeError:
            return self.count

    @property
    def count(self):
        """
        Количество объектов в текущем подзапросе
        :return:
        """
        return len(self._items)

    @property
    def is_number(self):
        """
        Результат запроса - единичное число
        :return:
        """
        return isinstance(self.raw_data, int)

    @property
    def get_number(self):
        if self.is_number:
            return self.raw_data
