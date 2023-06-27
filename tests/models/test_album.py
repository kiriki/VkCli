import tempfile

import pytest
from tests.credentials import VK_CREDS
from vk_cli import VKCredentials
from vk_cli.models import VKPhotoAlbum

VKCredentials.set(VK_CREDS)


@pytest.fixture
def album() -> VKPhotoAlbum:
    # return VKPhotoAlbum(owner_id=1, object_id=-7).load()
    return VKPhotoAlbum('-67940544_203553656').load()


def test_album_type(album: VKPhotoAlbum):
    assert isinstance(album, VKPhotoAlbum)


def test_album_pros(album: VKPhotoAlbum):
    assert album.id == 203553656
    assert album.album_id == 203553656
    assert album.owner_id == -67940544


def test_album_titlename(album: VKPhotoAlbum):
    assert album.title == 'Биеннале современного искусства "Манифеста 10"'


def test_album_download(album: VKPhotoAlbum):
    with tempfile.TemporaryDirectory() as temp_dir:
        # pass
        album.download(dl_path=temp_dir)
