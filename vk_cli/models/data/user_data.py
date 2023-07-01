import datetime
from dataclasses import dataclass

from vk_cli.models.data.vk_object_data import VKObjectData


class UserFields:
    ABOUT = 'about'  # О себе
    ACTIVITIES = 'activities'  # Деятельность
    BDATE = 'bdate'  # Дата рождения
    BLACKLISTED = 'blacklisted'
    BLACKLISTED_BY_ME = 'blacklisted_by_me'
    BOOKS = 'books'
    CAN_POST = 'can_post'
    CAN_SEE_ALL_POSTS = 'can_see_all_posts'
    CAN_SEE_AUDIO = 'can_see_audio'
    CAN_SEND_FRIEND_REQUEST = 'can_send_friend_request'
    CAN_WRITE_PRIVATE_MESSAGE = 'can_write_private_message'
    CAREER = 'career'  # карьера
    CITY = 'city'  # город
    COMMON_COUNT = 'common_count'  # общих друзей
    CONNECTIONS = 'connections'
    CONTACTS = 'contacts'
    COUNTERS = 'counters'
    COUNTRY = 'country'
    CROP_PHOTO = 'crop_photo'
    DOMAIN = 'domain'  # короткий адрес страницы
    EDUCATION = 'education'
    EXPORTS = 'exports'
    FOLLOWERS_COUNT = 'followers_count'
    FRIEND_STATUS = 'friend_status'
    GAMES = 'games'
    HAS_MOBILE = 'has_mobile'
    HAS_PHOTO = 'has_photo'
    HOME_TOWN = 'home_town'
    INTERESTS = 'interests'
    IS_FAVORITE = 'is_favorite'
    IS_FRIEND = 'is_friend'
    IS_HIDDEN_FROM_FEED = 'is_hidden_from_feed'
    LAST_SEEN = 'last_seen'
    MAIDEN_NAME = 'maiden_name'
    MILITARY = 'military'
    MOVIES = 'movies'
    MUSIC = 'music'
    NICKNAME = 'nickname'
    OCCUPATION = 'occupation'
    ONLINE = 'online'
    PERSONAL = 'personal'
    PHOTO_50 = 'photo_50'
    PHOTO_100 = 'photo_100'
    PHOTO_200 = 'photo_200'
    PHOTO_200_ORIG = 'photo_200_orig'
    PHOTO_400_ORIG = 'photo_400_orig'
    PHOTO_ID = 'photo_id'
    PHOTO_MAX = 'photo_max'
    PHOTO_MAX_ORIG = 'photo_max_orig'
    QUOTES = 'quotes'
    RELATIVES = 'relatives'
    RELATION = 'relation'
    SCHOOLS = 'schools'
    SCREEN_NAME = 'screen_name'
    SEX = 'sex'
    SITE = 'site'
    STATUS = 'status'
    TIMEZONE = 'timezone'
    TRENDING = 'trending'
    TV = 'tv'
    UNIVERSITIES = 'universities'
    VERIFIED = 'verified'
    WALL_DEFAULT = 'wall_default'

    NAME_CASES = ['nom', 'gen', 'dat', 'acc', 'ins', 'abl']

    ALL_FIELDS = [
        ABOUT,
        ACTIVITIES,
        BDATE,
        BLACKLISTED,
        BLACKLISTED_BY_ME,
        BOOKS,
        CAN_POST,
        CAN_SEE_ALL_POSTS,
        CAN_SEE_AUDIO,
        CAN_SEND_FRIEND_REQUEST,
        CAN_WRITE_PRIVATE_MESSAGE,
        CAREER,
        CITY,
        COMMON_COUNT,
        CONNECTIONS,
        CONTACTS,
        COUNTERS,
        COUNTRY,
        CROP_PHOTO,
        DOMAIN,
        EDUCATION,
        EXPORTS,
        FOLLOWERS_COUNT,
        FRIEND_STATUS,
        GAMES,
        HAS_MOBILE,
        HAS_PHOTO,
        HOME_TOWN,
        INTERESTS,
        IS_FAVORITE,
        IS_FRIEND,
        IS_HIDDEN_FROM_FEED,
        LAST_SEEN,
        MAIDEN_NAME,
        MILITARY,
        MOVIES,
        MUSIC,
        NICKNAME,
        OCCUPATION,
        ONLINE,
        PERSONAL,
        PHOTO_50,
        PHOTO_100,
        PHOTO_200_ORIG,
        PHOTO_200,
        PHOTO_400_ORIG,
        PHOTO_ID,
        PHOTO_MAX,
        PHOTO_MAX_ORIG,
        QUOTES,
        RELATIVES,
        RELATION,
        SCHOOLS,
        SCREEN_NAME,
        SEX,
        SITE,
        STATUS,
        TIMEZONE,
        TRENDING,
        TV,
        UNIVERSITIES,
        VERIFIED,
        WALL_DEFAULT,
    ]

    MAIN = [
        BDATE,
        BLACKLISTED,
        BLACKLISTED_BY_ME,
        CAN_POST,
        CAN_SEE_ALL_POSTS,
        CAN_SEE_AUDIO,
        CAN_SEND_FRIEND_REQUEST,
        CAN_WRITE_PRIVATE_MESSAGE,
        CITY,
        COUNTRY,
        DOMAIN,
        FOLLOWERS_COUNT,
        FRIEND_STATUS,
        IS_FRIEND,
        IS_HIDDEN_FROM_FEED,
        NICKNAME,
        PHOTO_100,
        SEX,
        SITE,
        STATUS,
    ]


@dataclass
class LastSeen:
    time: datetime.datetime
    platform: int


@dataclass
class UserDataActivity(VKObjectData):
    # activity
    online: bool  # информация о том, находится ли пользователь сейчас на сайте.
    online_app: int | None  # идентификатор мобильного приложения
    last_seen: LastSeen  # время последнего посещения
    online_mobile: bool | None = False  # пользователь использует мобильное приложение либо мобильную версию


@dataclass
class UserData(VKObjectData):
    # personal
    first_name: str  # имя
    last_name: str  # фамилия
    nickname: str | None  # никнейм (отчество) пользователя.
    maiden_name: str | None  # девичья фамилия.
    bdate: str | None  # дата рождения. Возвращается в формате D.M.YYYY или D.M (если год рождения скрыт).
    sex: int | None  # пол. 1 — женский; 2 — мужской; 0 — пол не указан.
    relation: int | None  # семейное положение
    domain: str | None  # короткий адрес страницы или "id"+user_id, например, id35828305.
    screen_name: str | None  # короткое имя страницы.
    relatives: list | None  # список родственников
    status: str | None  # статус пользователя
    status_audio: dict | None  # информация о текущей проигрываемой композиции
    is_closed: bool | None  # скрыт ли профиль пользователя настройками приватности.
    deactivated: str | None  # возвращается, если страница пользователя удалена или заблокирована

    # contacts
    country: dict | None  # информация о стране, указанной на странице пользователя в разделе «Контакты»
    city: dict | None  # информация о городе, указанном на странице пользователя в разделе «Контакты»
    home_town: str | None  # название родного города.
    contacts: dict | None  # информация о телефонных номерах пользователя
    site: str | None  # адрес сайта, указанный в профиле.
    connections: dict | None
    # данные об указанных в профиле сервисах пользователя, таких как: skype, facebook, twitter, livejournal,
    # instagram. Для каждого сервиса возвращается отдельное поле с типом string, содержащее никнейм пользователя.
    # Например, "instagram": "username".

    # flags
    has_mobile: bool | None  # известен ли номер мобильного телефона пользователя.
    has_photo: bool | None  # установил ли пользователь фотографию для профиля.
    trending: bool | None  # есть ли на странице пользователя «огонёк».
    verified: bool | None  # верифицирована ли страница пользователя

    # related current user
    friend_status: int | None  # статус дружбы с пользователем.
    common_count: int | None  # количество общих друзей с текущим пользователем.

    can_access_closed: bool | None  # может ли текущий пользователь видеть профиль при is_closed например, он есть в друзьях).
    blacklisted: bool | None  # находится ли текущий пользователь в черном списке.
    blacklisted_by_me: bool | None  # находится ли пользователь в черном списке у текущего пользователя.
    can_post: bool | None  # информация о том, может ли текущий пользователь оставлять записи на стене.
    can_see_all_posts: bool | None  # может ли текущий пользователь видеть чужие записи на стене
    can_see_audio: bool | None  # может ли текущий пользователь видеть аудиозаписи.
    can_send_friend_request: bool | None
    # информация о том, будет ли отправлено уведомление пользователю о заявке в друзья от текущего пользователя.
    can_write_private_message: bool | None  # может ли текущий пользователь отправить личное сообщение
    is_favorite: bool | None  # есть ли пользователь в закладках у текущего пользователя
    is_friend: bool | None  # является ли пользователь другом текущего пользователя
    is_hidden_from_feed: bool | None  # скрыт ли пользователь из ленты новостей текущего пользователя.

    # photo
    # url фотографий пользователя, заданной ширины. В случае отсутствия у пользователя
    # фотографии возвращается https://vk.com/images/camera_{width}.png.
    photo_50: str | None
    photo_100: str | None
    photo_200: str | None
    photo_400: str | None
    photo_max: str | None
    photo_200_orig: str | None
    photo_400_orig: str | None
    photo_max_orig: str | None

    photo_id: str | None  # str_id главной фотографии профиля пользователя в формате {user_id}_{photo_id}
    crop_photo: dict | None  # данные о точках, по которым вырезаны профильная и миниатюрная фотографии пользователя

    # social
    education: dict | None  # информация о высшем учебном заведении пользователя
    career: list | None  # информация о карьере пользователя
    occupation: dict | None  # информация о текущем роде занятия пользователя
    schools: list | None  # список школ, в которых учился пользователь
    universities: list | None  # список вузов, в которых учился пользователь.
    military: list | None  # информация о военной службе пользователя.

    # about / profile
    personal: dict | None  # информация о полях из раздела «Жизненная позиция».
    about: str | None  # содержимое поля «О себе» из профиля.
    activities: str | None  # содержимое поля «Деятельность» из профиля.
    books: str | None  # содержимое поля «Любимые книги» из профиля пользователя.
    games: str | None  # содержимое поля «Любимые игры» из профиля.
    movies: str | None  # содержимое поля «Любимые фильмы» из профиля пользователя.
    music: str | None  # содержимое поля «Любимая музыка» из профиля пользователя.
    interests: str | None  # содержимое поля «Интересы» из профиля.
    quotes: str | None  # любимые цитаты.
    tv: str | None  # любимые телешоу.

    # activity
    online: bool | None  # информация о том, находится ли пользователь сейчас на сайте.
    online_mobile: bool | None  # пользователь использует мобильное приложение либо мобильную версию
    online_app: int | None  # идентификатор мобильного приложения
    last_seen: dict | None  # время последнего посещения

    # counters
    followers_count: int | None  # количество подписчиков пользователя.
    counters: dict | None  # количество различных объектов у пользователя.
    # Поле возвращается только в методе users.get при запросе информации об одном пользователе, с передачей
    # пользовательского access_token.

    # other
    timezone: int | None  # временная зона. Только при запросе информации о текущем пользователе.
    exports: dict | None  # внешние сервисы, в которые настроен экспорт (twitter, facebook, livejournal, instagram).
    wall_default: str | None  # режим стены по умолчанию. Возможные значения: owner, all.
    lists: list | None

    # разделенные запятой идентификаторы списков друзей, в которых состоит пользователь. поле доступно только для
    # метода friends.get.
