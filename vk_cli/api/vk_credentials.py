from . import vk_const


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ApiCredentials(metaclass=Singleton):
    """
    Параметры доступа к api vk.com
    """
    credentials = {}

    def set(self, credentials):
        self.credentials = credentials

    # @property
    def get_access_token(self):
        assert self.credentials
        return self.credentials.get(vk_const.ACCESS_TOKEN)

    # @property
    def get_api_version(self):
        assert self.credentials
        return self.credentials.get(vk_const.API_VERSION)


# singleton параметры доступа к vk api
VKCredentials = ApiCredentials()
