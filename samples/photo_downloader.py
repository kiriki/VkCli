from tests.credentials import VK_CREDS
from vk_cli import VKCredentials
from vk_cli.models import VKPhotoAlbum

VKCredentials.set(VK_CREDS)


def main():
    dl_folder = '/home/user/tmp/vkdls'

    # album = VKPhotoAlbum(owner_id=1, object_id=-7).open()
    # album = VKPhotoAlbum(owner_id=-67940544, object_id=203553656).open()
    album = VKPhotoAlbum('-67940544_203553656').open()

    print(album)

    album.download(dl_folder)


if __name__ == '__main__':
    main()
