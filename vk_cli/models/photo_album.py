from collections.abc import Iterator

from .. import api
from . import VKPhoto
from .data import PhotoAlbumData
from .lister import ModelLister
from .vk_object import VKobjectOwned

# from .vk_privacy import VkPrivacy


class VKPhotoAlbum(VKobjectOwned):
    type = 'album'
    vk_data_class = PhotoAlbumData
    do_stat = False
    system_albums = {-6: '0', -7: '00', -15: '000'}

    def __init__(self, string_id=None, object_id=None, owner_id=None) -> None:
        super().__init__(string_id=string_id, owner_id=owner_id, object_id=object_id)

        self._likes_count = -1
        self._privacy_view = None
        self._privacy_comment = None
        self.rev = False

    def _get_vk_data(self):
        # todo выделить в поле get_request?
        request = api.photos.get_albums(owner_id=self.owner_id, album_ids=self.album_id)
        a = request.get_invoke_result()
        return a.single

    @staticmethod
    def create(title, description='', group_id=None):
        """
        Создаёт новый пустой альбом для фотографий на сайте VK.com
        :param description: описание альбома
        :param title: название альбома
        :param group_id: идентификатор сообщества, в котором создаётся альбом
        :rtype: VKPhotoAlbum
        """
        # todo privacy

        request = api.photos.create_album(title=title, group_id=group_id, description=description)
        result = request.get_invoke_result()

        return VKPhotoAlbum.from_data(result.single)

    def __iter__(self) -> Iterator[VKPhoto]:
        """
        Проход по всем фото в альбоме
        """
        yield from self.photos

    @property
    def photos(self):
        request = api.photos.get(owner_id=self.owner_id, album_id=self.album_id, rev=self.rev)
        return ModelLister(request, step=500)

    @property
    def is_editable(self):
        return self.vk_data.privacy_view is not None

    def download(self, dl_folder):
        """
        Скачивает фотографии из альбома в папку dl_folder
        :param dl_folder:
        """
        import os

        dl_folder = os.path.join(dl_folder, self._get_dl_folder_name())
        if not os.path.exists(dl_folder):
            os.makedirs(dl_folder)

        for i, photo in enumerate(self, 1):
            photo.download(dl_folder, i)

    def _get_dl_folder_name(self):
        return f'{self.owner_id}_{self.album_id} ({self.title})'

    def dl_file(self, file):
        import codecs

        with codecs.open(file, 'w', encoding='utf-8') as ifile:
            for photo in self:
                # ifile.write(photo._get_largest_url()+'\r\n')
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
    def album_id(self):
        return self.id

    @property
    def title(self):
        """
        Название альбома. Получение/установка заголовка альбома с фото на сайте vk.com
        """
        return self.vk_data.title

    @title.setter
    def title(self, new_title):
        if self._edit(title=new_title):
            self.vk_data.title = new_title

    @property
    def description(self):
        """
        Описание альбома. Получение/установка заголовка альбома с фото на сайте vk.com
        """
        return self.vk_data.description

    # @property
    # def privacy_view(self):
    #     if self._privacy_view is None:
    #         self._privacy_view = VkPrivacy(self.vk_data.privacy_view)
    #     return self._privacy_view

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
    def size(self):
        return self.vk_data.size

    @property
    def like_index(self):
        if self.do_stat and self.size:
            return int(self.likes_count * 100.0 / self.size)
        else:
            return -1

    @property
    def likes_count(self):
        if self.do_stat and self._likes_count == -1:
            self._likes_count = sum([p.like.count for p in self])

        return self._likes_count

    @property
    def url(self):
        url_base = super().url
        owner = self.vk_data.owner_id
        album = self.vk_data.id
        if album in self.system_albums:
            album = self.system_albums[album]

        strid = f'{self.type}{owner}_{album}'
        url = f'{url_base}{strid}'
        return url

    def __str__(self):
        if self.do_stat:
            out = f'[pl:{self.size}/{self.likes_count} - {self.like_index}] {self.title} ({self.url})'
        else:
            out = f'{self.title} [{self.size} photos] - {self.url}'
        return out
