from collections.abc import Iterator
from pathlib import Path
from typing import Self

from vk_cli import api

from . import VKPhoto
from .data import PhotoAlbumData
from .lister import ModelLister
from .vk_object import VKobjectOwned


class VKPhotoAlbum(VKobjectOwned):
    vk_object_type = 'album'
    vk_data_class = PhotoAlbumData
    vk_data: PhotoAlbumData | None
    do_stat = False
    system_albums = {-6: '0', -7: '00', -15: '000'}

    def __init__(self, string_id: str | None = None, object_id: int | None = None, owner_id: int | None = None) -> None:
        super().__init__(string_id=string_id, owner_id=owner_id, object_id=object_id)

        self._likes_count = -1
        self._privacy_view = None
        self._privacy_comment = None
        self.rev = False

    def _get_vk_data(self) -> dict:
        # TODO выделить в поле get_request?
        request = api.photos.get_albums(owner_id=self.owner_id, album_ids=self.album_id)
        a = request.get_invoke_result()
        return a.single

    @classmethod
    def create(cls, title: str, description: str = '', group_id: int | None = None) -> Self:
        """
        Создаёт новый пустой альбом для фотографий на сайте VK.com
        :param description: описание альбома
        :param title: название альбома
        :param group_id: идентификатор сообщества, в котором создаётся альбом
        """
        # TODO privacy

        request = api.photos.create_album(title=title, group_id=group_id, description=description)
        result = request.get_invoke_result()

        return cls.from_data(result.single)

    def __iter__(self) -> Iterator[VKPhoto]:
        """
        Проход по всем фото в альбоме
        """
        yield from self.photos

    @property
    def photos(self) -> ModelLister:
        request = api.photos.get(owner_id=self.owner_id, album_id=self.album_id, rev=self.rev)
        return ModelLister(request, step=500)

    @property
    def is_editable(self) -> bool:
        return self.vk_data.privacy_view is not None

    def download(self, dl_path: str | Path) -> None:
        """
        Скачивает фотографии из альбома в папку dl_folder
        """
        dl_path = Path(dl_path)
        dl_path = dl_path / self._get_dl_folder_name()
        dl_path.mkdir(parents=True, exist_ok=True)
        for i, photo in enumerate(self, 1):
            photo.download(dl_path, i)

    def _get_dl_folder_name(self) -> str:
        return f'{self.owner_id}_{self.album_id} ({self.title})'

    def dl_file(self, file):
        import codecs

        with codecs.open(file, 'w', encoding='utf-8') as ifile:
            for photo in self:
                ifile.write(photo.out_html())

    def delete(self):
        """
        Удаление фотоальборма
        :rtype: bool
        """
        if self.owner_id[0] == '-':
            return api.photos.delete_album(self.album_id, self.owner_id[1:])
        else:
            return api.photos.delete_album(self.album_id)

    def _edit(self, **kwargs):
        return api.photos.edit_album(album_id=self.album_id, owner_id=self.owner_id, **kwargs)

    @property
    def album_id(self) -> int:
        return self.id

    @property
    def title(self) -> str:
        """
        Название альбома. Получение/установка заголовка альбома с фото на сайте vk.com
        """
        return self.vk_data.title

    @title.setter
    def title(self, new_title: str) -> None:
        if self._edit(title=new_title):
            self.vk_data.title = new_title

    @property
    def description(self) -> str:
        """
        Описание альбома. Получение/установка заголовка альбома с фото на сайте vk.com
        """
        return self.vk_data.description

    # @property
    # def privacy_view(self):
    #     if self._privacy_view is None:

    @property
    def created(self):
        """
        Описание альбома. Получение/установка заголовка альбома с фото на сайте vk.com
        """
        return self.vk_data.created

    @property
    def updated(self):
        """
        Описание альбома. Получение/установка заголовка альбома с фото на сайте vk.com
        """
        return self.vk_data.updated

    @property
    def size(self) -> int:
        return self.vk_data.size

    @property
    def like_index(self) -> int:
        if self.do_stat and self.size:
            return int(self.likes_count * 100.0 / self.size)
        return -1

    @property
    def likes_count(self) -> int:
        if self.do_stat and self._likes_count == -1:
            self._likes_count = sum([p.like.count for p in self])

        return self._likes_count

    @property
    def url(self) -> str:
        url_base = super().url
        owner = self.vk_data.owner_id
        album = self.vk_data.id
        if album in self.system_albums:
            album = self.system_albums[album]

        strid = f'{self.vk_object_type}{owner}_{album}'
        return f'{url_base}{strid}'

    def __str__(self) -> str:
        if self.do_stat:
            out = f'[pl:{self.size}/{self.likes_count} - {self.like_index}] {self.title} ({self.url})'
        else:
            out = f'{self.title} [{self.size} photos] - {self.url}'
        return out
