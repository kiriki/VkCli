import logging

from vk_cli import api as vkapi, VK
from vk_cli.api.vk_api_error import VKEAccessError
from vk_cli.models import ModelLister

log = logging.getLogger(__name__)


class PhotoCollection:
    """
    Used for interaction with photos and photo albums of the user or group
    * getting available albums and photos
    * todo: creating and editing albums
    * todo: uploading, editing photos
    """

    def __init__(self, vk: VK, owner_id: int) -> None:
        self._vk = vk
        self.owner_id = owner_id
        self._albums = []

    def __repr__(self) -> str:
        return f'photos in collection {self.owner_id}'

    @property
    def albums(self) -> ModelLister:
        """
        Generator for getting all photos albums for the current user or group
        """
        request = vkapi.photos.get_albums(self._vk, owner_id=self.owner_id, need_system=True, album_ids=-7)
        return ModelLister(request)

    @property
    def photos(self) -> ModelLister:
        """
        Generator for getting all available photos for the current user or group
        """
        request = vkapi.photos.get_all(self._vk, owner_id=self.owner_id)
        return ModelLister(request)

    @property
    def tags(self) -> ModelLister | None:
        """
        Generator for getting photos with pending tags for the current user
        """
        if self.owner_id < 0:
            log.info('tagged photos only for users')
            return None

        request = vkapi.photos.get_user_photos(user_id=self.owner_id)
        try:
            return ModelLister(request)
            # for photo in ModelLister(request):
            #     yield photo
        except VKEAccessError:
            log.error("Access denied. This user doesn't show his tagged photos")

    @property
    def tags_new(self):
        """
        Generator for getting photos with pending tags for the current user
        """
        if self.owner_id != VKApi.current_user_id:
            log.info('tagged photos only for current user')
            return

    def create_album(self, title: str, description: str = '') -> None:
        """
        Создание фотоальбома
        """
