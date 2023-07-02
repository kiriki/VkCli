from __future__ import annotations

from abc import ABC

from vk_cli.api.misc import get_params
from vk_cli.api.vk_request import VKRequest

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vk_cli import VK


class VKApiBase(ABC):
    method_group = None
    cls_name_prefix = 'VKApi'

    def __init__(self) -> None:
        class_name = self.__class__.__name__
        self.method_group = class_name.lower()[len(self.cls_name_prefix):]

    @classmethod
    def build_request(cls, vk: VK, method_name: str, local_vars: dict) -> VKRequest:
        """
        Формирование экземпляра VKRequest на основании имени метода и входных параметров

        :param vk:
        :param method_name: API method name
        :param local_vars:
        """
        from vk_cli import VK
        assert isinstance(vk, VK), f"is required to set 'vk' value for class '{cls.__name__}', {vk=}"
        assert cls.method_group is not None, f"is required to set 'method_group' value for class '{cls.__name__}'"

        method_group_name = '.'.join(filter(lambda a: a, [cls.method_group, method_name]))
        params = get_params(local_vars)

        return VKRequest(vk, method_group_name, params)


def raw_result(original_func):
    """
    Исходный результат выполнения сформированного запроса

    :param original_func:
    :return:
    """

    def wraped(self, *args, **kwargs):
        request = original_func(self, *args, **kwargs)
        assert isinstance(request, VKRequest)
        return request.invoke_response()

    return wraped


def build_request(method_name: str, model_name: str | None = None):
    """
    Create VKRequest with optional model binding for serial objects retrieving

    :param method_name: VK API method name
    :param model_name: model class name
    :return: function
    """
    print('build_request2')

    def wp_dec(*args):
        print('build_request2.wp_dec')

        # def wp_func(cls, vk: VK, **kwargs):
        def wp_func(cls, vk: VK, **params):
            print('build_request2.wp_dec.wp_func')
            request = cls.build_request(vk, method_name, params)

            if model_name is not None:
                request.bind_model(model_name)

            return request

        return wp_func

    return wp_dec


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
