CLIENT_ID = 'client_id'
CLIENT_SECRET = 'client_secret'
ACCESS_TOKEN = 'access_token'
ACCESS_TOKEN_SECURE = 'access_token_secure'
API_VERSION = 'v'
HTTPS = 'https'

PLATFORM_UNKNOWN = 0
PLATFORM_MOBILE = 1  # Мобильная версия сайта или неопознанное мобильное приложение
PLATFORM_IPHONE = 2  # Официальное приложение для iPhone
PLATFORM_IPAD = 3  # Официальное приложение для iPad
PLATFORM_ANDROID = 4  # Официальное приложение для Android
PLATFORM_WPHONE = 5  # Официальное приложение для Windows Phone
PLATFORM_WINDOWS = 6  # Официальное приложение для Windows 8
PLATFORM_WEB = 7  # Полная версия сайта или неопознанное приложение

PLATFORMS = {
    PLATFORM_UNKNOWN: 'unknown platform',
    PLATFORM_MOBILE: 'mobile',
    PLATFORM_IPHONE: 'iphone',
    PLATFORM_IPAD: 'ipad',
    PLATFORM_ANDROID: 'android',
    PLATFORM_WPHONE: 'wphone',
    PLATFORM_WINDOWS: 'windows',
    PLATFORM_WEB: 'web',
}
