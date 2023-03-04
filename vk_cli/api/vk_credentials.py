from . import vk_const

DEFAULT_API_VERSION = '5.131'


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class ApiCredentials(metaclass=Singleton):
    """
    Параметры доступа к api vk.com
    """

    credentials = {}

    def set(self, credentials: dict):
        self.credentials = credentials

    @property
    def access_token(self):
        assert self.credentials, 'required to set credentials with "VKCredentials.set(CRED_DATA)"'

        return self.credentials.get(vk_const.ACCESS_TOKEN)

    @property
    def api_version(self):
        assert self.credentials, 'required to set credentials with "VKCredentials.set(CRED_DATA)"'

        return self.credentials.get(vk_const.API_VERSION, DEFAULT_API_VERSION)

    @property
    def lang(self):
        assert self.credentials, 'required to set credentials with "VKCredentials.set(CRED_DATA)"'

        return self.credentials.get(vk_const.LANG)


# singleton параметры доступа к vk api
VKCredentials = ApiCredentials()
