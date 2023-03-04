import html
from abc import ABCMeta, abstractmethod
from copy import copy

from dacite import from_dict

from .data.vk_object_data import VKObjectData


class VKobject(metaclass=ABCMeta):
    vk_data_class = VKObjectData
    type = None

    class InvalidObjectId(Exception):
        pass

    def __init__(self, string_or_object_id):
        self._id = None
        self.vk_data = None

        if isinstance(string_or_object_id, int):
            self._id = string_or_object_id

        elif isinstance(string_or_object_id, str):
            self._init_from_string_id(string_or_object_id)

    @classmethod
    def from_data(cls, data: dict):
        pre = cls(None)
        pre._init_from_json(data)
        return pre

    def _init_from_string_id(self, str_id):
        if str_id[1:].isdigit():  # like '-38141560'
            self._id = int(str_id)

        else:  # like 'short_name'
            self._domain = str_id

    @property
    def string_id(self):
        if self.id:
            return str(self.id)

    @property
    def url(self):
        url_base = 'https://vk.com/'
        return url_base

    @property
    def is_init(self):
        return self.vk_data is not None

    def __eq__(self, other):
        return self.id == other.id and self.type == other.type

    @abstractmethod
    def _get_vk_data(self):
        """
        To override
        получение JSON-данных для единичного объекта с сервера vk
        """
        raise NotImplementedError

    def open(self):
        """
        Получение детальной информации по объекту из VK и инициализация vk_data
        """
        data = self._get_vk_data()
        assert isinstance(data, dict)
        self._init_from_json(data)
        return self

    def reload(self):
        self.open()

    def _init_from_json(self, data):
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
    def id(self):
        return self._id or self.vk_data and self.vk_data.id

    def get_source_data(self):
        return self.vk_data and self.vk_data.source


class VKobjectOwned(VKobject, metaclass=ABCMeta):
    _owner_id = None

    def __init__(self, string_id=None, owner_id=None, object_id=None):
        super().__init__(string_id or object_id)
        self._owner_id = self._owner_id or owner_id

    def _init_from_string_id(self, str_id):
        if '_' in str_id:  # like '-38141560_168748493'
            self._owner_id, self._id = map(int, str_id.split('_'))

        elif str_id[1:].isdigit():  # like '-38141560'
            self._id = int(str_id)

        else:  # like 'short_name'
            self._domain = str_id

    @property
    def owner_id(self):
        return self._owner_id or self.vk_data.owner_id

    @property
    def string_id(self):
        if self.id and self.owner_id:
            return f'{self.owner_id}_{self.id}'
