import tempfile

import pytest

from tests.credentials import VK_CREDS
from vk_cli import VKCredentials, VK
from vk_cli.models import VKPhotoAlbum

VKCredentials.set(VK_CREDS)


@pytest.fixture
def vk() -> VK:
    return VK(**VK_CREDS)


@pytest.fixture
def album(vk: VK) -> VKPhotoAlbum:
    return VKPhotoAlbum(vk, '-67940544_203553656').load()


def test_album_type(album: VKPhotoAlbum) -> None:
    assert isinstance(album, VKPhotoAlbum)


def test_album_pros(album: VKPhotoAlbum) -> None:
    assert album.id == 203553656
    assert album.album_id == 203553656
    assert album.owner_id == -67940544


def test_album_titlename(album: VKPhotoAlbum) -> None:
    assert album.title == 'Биеннале современного искусства "Манифеста 10"'


def test_album_download(album: VKPhotoAlbum) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        album.download(dl_path=temp_dir)
