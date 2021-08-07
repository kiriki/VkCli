from abc import ABC

from ..misc import get_params
from ..vk_request import VKRequest


class VKApiBase(ABC):
    method_group = None
    cls_name_prefix = 'VKApi'

    def __init__(self):
        class_name = self.__class__.__name__
        self.method_group = class_name.lower()[len(self.cls_name_prefix):]

    @classmethod
    def build_request(cls, method_name, local_vars) -> VKRequest:
        """
        Формирование экземпляра VKRequest на основании имени метода и входных параметров
        :param method_name:
        :param local_vars:
        """
        assert cls.method_group is not None, \
            f"is required to set 'method_group' value for class '{cls.__name__}'"

        method_group_name = '.'.join(filter(lambda a: a, [cls.method_group, method_name]))
        params = get_params(local_vars)

        return VKRequest(method_group_name, params)


def raw_result(original_func):
    """
    исходный результат выполнения сформированного запроса
    :param original_func:
    :return:
    """

    def wraped(self, *args, **kwargs):
        request = original_func(self, *args, **kwargs)
        assert isinstance(request, VKRequest)
        return request.invoke_response()

    return wraped


def with_model(class_name):
    """
    Привязка запоса к модели для получения экземпляров на основании результата запроса
    :param class_name:
    :return:
    """

    def wp_dec(api_function):
        def wp_func(*args, **kwargs):
            request = api_function(*args, **kwargs)
            request.bind_model(class_name)

            return request

        return wp_func

    return wp_dec
