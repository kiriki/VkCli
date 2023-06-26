import html
from abc import ABCMeta, abstractmethod
from copy import copy
from typing import Self

from dacite import from_dict

from .data.vk_object_data import VKObjectData, VKOwnedObjectData


class VKobject(metaclass=ABCMeta):
    vk_data_class = VKObjectData
    vk_object_type = None

    class InvalidObjectId(Exception):
        pass

    def __init__(self, string_or_object_id: int | str) -> None:
        self._id = None
        self.vk_data: VKObjectData | None = None

        if isinstance(string_or_object_id, int):
            self._id = string_or_object_id

        elif isinstance(string_or_object_id, str):
            self._init_from_string_id(string_or_object_id)

    @classmethod
    def from_data(cls, data: dict) -> Self:
        pre = object.__new__(cls)
        pre._init_from_json(data)
        return pre

    def _init_from_string_id(self, str_id: str) -> None:
        if str_id[1:].isdigit():  # like '-38141560'
            self._id = int(str_id)

        else:  # like 'short_name'
            self._domain = str_id

    @property
    def string_id(self) -> str | None:
        if self.id:
            return str(self.id)
        return None

    @property
    def url(self) -> str:
        return 'https://vk.com/'

    @property
    def is_init(self) -> bool:
        return self.vk_data is not None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented

        return self.id == other.id and self.vk_object_type == other.vk_object_type

    @abstractmethod
    def _get_vk_data(self) -> None:
        """
        To override
        получение JSON-данных для единичного объекта с сервера vk
        """
        raise NotImplementedError

    def open(self) -> Self:
        """
        Получение детальной информации по объекту из VK и инициализация vk_data
        """
        data = self._get_vk_data()
        assert isinstance(data, dict)
        self._init_from_json(data)
        return self

    def reload(self) -> None:
        self.open()

    def _init_from_json(self, data) -> Self:
        """
        Инициализация по данным JSON
        :param data: словарь с данными об объекте, полученный в результате запроса через API VK
        """

        data = html.unescape(data)

        _data = copy(data)
        _data['source'] = data

        kwargs = {
            'data_class': self.vk_data_class,
            'data': _data,
        }

        if hasattr(self.vk_data_class.Meta, 'config'):
            kwargs['config'] = self.vk_data_class.Meta.config

        self.vk_data = from_dict(**kwargs)

        return self

    @property
    def id(self) -> int:
        return self._id or self.vk_data and self.vk_data.id

    def get_source_data(self):
        return self.vk_data and self.vk_data.source


class VKobjectOwned(VKobject, metaclass=ABCMeta):
    vk_data_class = VKOwnedObjectData

    def __init__(self, string_id: str | None = None, owner_id: int | None = None, object_id: int | None = None) -> None:
        super().__init__(string_id or object_id)

        self.vk_data: VKOwnedObjectData | None = None
        self._owner_id: int | None = self._owner_id or owner_id

    def _init_from_string_id(self, str_id: str) -> None:
        if '_' in str_id:  # like '-38141560_168748493'
            self._owner_id, self._id = map(int, str_id.split('_'))

        elif str_id[1:].isdigit():  # like '-38141560'
            self._id = int(str_id)

        else:  # like 'short_name'
            self._domain = str_id

    @property
    def owner_id(self) -> int:
        return self._owner_id or self.vk_data.owner_id

    @property
    def string_id(self) -> str | None:
        if self.id and self.owner_id:
            return f'{self.owner_id}_{self.id}'
        return None
