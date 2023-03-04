from ..api.vk_request import PartialRequest


class ModelLister:
    """
    Класс для получения всех экземпляров модели на основании базовго запроса и значений
    параметров offset и count
    """

    def __init__(self, request, step=200):
        assert request.is_binded

        self.partial_generator = PartialRequestsGenerator(request, step)

    def __iter__(self):
        # get all Models from associated partial requests
        for partial_request in self.partial_generator:
            response = partial_request.get_invoke_result()
            yield from response.model_generator()

    @property
    def ids_generator(self):
        for partial_request in self.partial_generator:
            response = partial_request.get_invoke_result()
            yield from response.ids_generator()

    @property
    def count(self):
        return self.partial_generator.total

    def __str__(self):
        return (
            f'[{self.partial_generator.request.binded_model.__name__}] {self.count} items '
            f'({self.count // self.partial_generator.step} pages by {self.partial_generator.step})'
        )


class PartialRequestsGenerator:
    """
    Используется для получения уточнённых запросов с указанным шагом
    """

    offset = 0

    def __init__(self, request, step):
        self.request = request  # base request
        self.step = step  # items per request
        self._p_requests = {}

        self.first_request = self._get_p_request(self.offset)  # used for get_total

    def __str__(self) -> str:
        m1 = self.request.binded_model.__name__
        m2 = self.first_request.binded_model.__name__
        assert m1 == m2
        return f'PartialRequestsGenerator by {self.step} items for request:\n\t{self.request} [{m1}]'

    @property
    def total(self):
        return self.first_request.get_invoke_result().total

    def _get_p_request(self, offset):
        try:
            return self._p_requests[offset]
        except KeyError:
            new = PartialRequest(self.request, self.step, offset)
            self._p_requests[offset] = new
            return new

    def __iter__(self):
        yield self.first_request
        last = self.first_request.invoked()
        self.offset += last.response.count

        # while self.offset < self.total:
        while last.response.count > 0:
            # while last.response.count == self.step:
            last = self._get_p_request(self.offset).invoked()  # todo кеширование
            yield last
            self.offset += last.response.count

        self.offset = 0
