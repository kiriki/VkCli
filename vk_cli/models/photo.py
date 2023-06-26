import os
from datetime import datetime

from vk_cli import api

from .data import PhotoData
from .vk_object import VKobjectOwned


class VKPhoto(VKobjectOwned):
    """
    Фотография ВК. Представление фотографии на сайте vk.com
    """

    vk_object_type = 'photo'
    vk_data_class = PhotoData

    size_vars = (2560, 1280, 807, 604, 130, 75)
    size_vars_old = ('w', 'z', 'y', 'x', 'm', 's')

    def _get_vk_data(self):
        request = api.photos.get_by_id(photos=self.string_id, photo_sizes=None, extended=True)
        result = request.get_invoke_result()
        return result.single

    def __repr__(self):
        return self.url

    @property
    def url(self):
        url_base = 'https://vk.com/photo'
        return f'{url_base}{self.owner_id}_{self.id}'

    @property
    def sizes(self):
        """
        image variants sizes dict
        :return:
        """
        return {i.type: i for i in self.vk_data.sizes}

    def out_html(self):
        rr = (
            f'<a href="https://vk.com/photo{self.vk_data.owner_id}_{self.vk_data.id}">'
            f'<img src="{self.vk_data.photo_max}"><br />'
            '</a>\r\n'
        )
        return rr

    def delete(self):
        """
        Удаление фотографии
        """

    def download(self, folder, name_counter=None, size_fmt=None):
        """
        Скачивание графического файла в указанную папку
        :param folder: папка назначения
        :param name_counter: опциональный счётчик для использования в имени файла
        :param size_fmt: формат размера по умолчанию максимальный 'max'
        :return:
        """
        from urllib.request import urlopen

        fname = self.as_attachment

        if isinstance(name_counter, int):
            fname = f'{name_counter:04d}. {fname}.jpg'

        fname_full = os.path.join(folder, fname)

        if os.path.isfile(fname_full):  # skip exists
            return

        with open(fname_full, 'wb') as f:
            url = self.get_image_url(size_fmt)
            u = urlopen(url)
            f.write(u.read())

    def get_image_url(self, size_fmt=None):
        """
        Ссылка на jpg заданного размера
        :param size_fmt: формат размера, если не указан используется максимальный
        :return:
        """
        if self.sizes:  # новый формат
            if size_fmt is None:
                sizez = 'smxopqryzw'[::-1]
                size = next(
                    self.sizes.get(s_l)
                    for s_l in sizez
                    if hasattr(self.sizes.get(s_l), 'url') and self.sizes.get(s_l).url
                )
            elif isinstance(size_fmt, tuple):
                size = self.sizes.get(size_fmt[0]) or self.sizes.get('x')
            else:
                raise TypeError('size_fmt None or tuple allowed ')
            return size.url

        else:  # старый формат
            if size_fmt is None:
                return self.vk_data.photo_max  # старый формат
            elif isinstance(size_fmt, tuple):
                return getattr(self.vk_data, f'photo_{size_fmt[1]}', 'error')
            else:
                raise TypeError('size_fmt None or tuple allowed ')

    def get_comments_data(self):
        comments_data = api.photos.get_comments(self.vk_data.id, owner_id=self.vk_data.owner_id, need_likes=True)
        return comments_data

    @property
    def date(self):
        return datetime.fromtimestamp(self.vk_data.date)

    @property
    def photo_max(self):
        try:
            return next(getattr(self, 'photo_' + str(s)) for s in self.size_vars if hasattr(self, 'photo_' + str(s)))
        except StopIteration:
            return None

    @property
    def as_attachment(self):
        # <type><owner_id>_<media_id>
        return f'{self.type}{self.owner_id}_{self.id}'
