from tests.credentials import VK_CREDS
from vk_cli import VK
from vk_cli.models import VKPhotoAlbum

vk = VK(**VK_CREDS)


def main():
    album = VKPhotoAlbum(vk, '-67940544_203553656').load()
    print(album)
    # dl_folder = '/home/user/tmp/vkdls'
    # album.download(dl_folder)


if __name__ == '__main__':
    main()
