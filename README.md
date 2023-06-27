**vk_cli** – vk.com API wrapper

```python
from vk_cli import VKCredentials
from vk_cli.models import VKPhotoAlbum

credentials = {
    'client_id': 1111,
    'access_token': '<token>'
}

VKCredentials.set(credentials)

album = VKPhotoAlbum(owner_id=1, object_id=-7).load()
print(album)

album.download(dl_path='/home/user/tmp/vkdls')
```
