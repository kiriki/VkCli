import datetime
from dataclasses import dataclass, field

from .vk_object_data import VKOwnedObjectData


@dataclass
class PhotoSize:
    type: str
    url: str
    width: int
    height: int


@dataclass
class PhotoData(VKOwnedObjectData):
    album_id: int  # идентификатор альбома, в котором находится фотография.
    user_id: int | None  # идентификатор пользователя, загрузившего фото (если фотография размещена в сообществе).
    # Для фотографий, размещенных от имени сообщества, user_id = 100.

    text: str  # текст описания фотографии.
    date: datetime.datetime  # дата добавления в формате Unixtime.
    width: int | None  # integer ширина оригинала фотографии в пикселах.
    height: int | None  # integer высота оригинала фотографии в пикселах.

    sizes: list[PhotoSize] = field(default_factory=list)  # массив с копиями изображения в разных размерах.
