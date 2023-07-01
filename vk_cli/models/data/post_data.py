import datetime
from dataclasses import dataclass, field

from vk_cli.models.data.attachents import DataAttachmentPhoto
from vk_cli.models.data.vk_object_data import VKOwnedObjectData


@dataclass
class PostDataComments:
    count: int  # количество комментариев;
    can_post: bool = (
        False  # информация о том, может ли текущий пользователь комментировать запись (1 — может, 0 — не может);
    )
    groups_can_post: bool = False  # информация о том, могут ли сообщества комментировать запись;
    can_close: bool = False  # может ли текущий пользователь закрыть комментарии к записи;
    can_open: bool = False  # может ли текущий пользователь открыть комментарии к записи.


@dataclass
class PostDataLikes:
    count: int  # число пользователей, которым понравилась запись;
    user_likes: bool  # наличие отметки «Мне нравится» от текущего пользователя (1 — есть, 0 — нет);
    can_like: bool
    # информация о том, может ли текущий пользователь поставить отметку «Мне нравится» (1 — может, 0 — не может);
    can_publish: bool
    # информация о том, может ли текущий пользователь сделать репост записи (1 — может, 0 — не может).


@dataclass
class PostDataReposts:
    count: int  # число пользователей, скопировавших запись;
    user_reposted: bool  # наличие репоста от текущего пользователя (1 — есть, 0 — нет).


@dataclass
class PostDataviews:
    count: int  # число просмотров записи.


@dataclass
class PostDataSource:
    """
    https://vk.com/dev/objects/post_source
    """

    type: str
    platform: str | None
    data: str | None
    url: str | None


@dataclass
class PostDataGeo:
    type: str  # тип места;
    coordinates: str  # координаты места;
    place: dict  # описание места (если оно добавлено). Объект места.


@dataclass
class PostData(VKOwnedObjectData):
    id: int  # идентификатор записи.
    owner_id: int | None  # идентификатор владельца стены, на которой размещена запись.
    from_id: int  # идентификатор автора записи (от чьего имени опубликована запись).
    to_id: int | None  # идентификатор автора записи (от чьего имени опубликована запись).
    created_by: int | None
    # идентификатор администратора, который опубликовал запись (возвращается только для сообществ при запросе с ключом
    # доступа администратора).
    date: datetime.datetime  # время публикации записи в формате unixtime.
    text: str  # текст записи.
    reply_owner_id: int | None  # идентификатор владельца записи, в ответ на которую была оставлена текущая.
    reply_post_id: int | None  # идентификатор записи, в ответ на которую была оставлена текущая.

    comments: PostDataComments  # информация о комментариях к записи
    likes: PostDataLikes | None  # информация о лайках к записи
    reposts: PostDataReposts | None  # информация о репостах записи («Рассказать друзьям»)
    views: PostDataviews | None  # информация о просмотрах записи. Объект с единственным полем:
    post_type: str  # тип записи, может принимать следующие значения: post, copy, reply, postpone, suggest.
    post_source: PostDataSource | None  # информация о способе размещения записи

    geo: PostDataGeo | None  # информация о местоположении
    signer_id: int | None
    # идентификатор автора, если запись была опубликована от имени сообщества и подписана пользователем;

    copy_history: list[dict] | None
    # массив, содержащий историю репостов для записи. Возвращается только в том случае, если запись является репостом.
    # Каждый из объектов массива, в свою очередь, является объектом-записью стандартного формата.

    is_favorite: bool  # если объект добавлен в закладки у текущего пользователя.
    friends_only: bool = False  # если запись была создана с опцией «Только для друзей».
    is_pinned: bool = False  # информация о том, что запись закреплена.
    can_edit: bool = False  # может ли текущий пользователь редактировать запись (1 — может, 0 — не может).
    can_pin: bool = False  # может ли текущий пользователь закрепить запись (1 — может, 0 — не может).
    can_delete: bool = False  # может ли текущий пользователь удалить запись (1 — может, 0 — не может).
    marked_as_ads: bool = False  # информация о том, содержит ли запись отметку "реклама" (1 — да, 0 — нет).

    attachments: list[DataAttachmentPhoto | dict] | None = field(default_factory=list)

    # медиавложения записи (фотографии, ссылки и т.п.).
