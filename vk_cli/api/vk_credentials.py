from typing import TypedDict

from . import vk_const

DEFAULT_API_VERSION = '5.131'


class VKCredentialsData(TypedDict):
    client_id: int
    client_secret: str | None
    access_token: str


class ApiCredentials:
    """
    Параметры доступа к api vk.com
    """

    def __init__(self, **kwargs: VKCredentialsData) -> None:
        if kwargs:
            self.credentials = kwargs

    def set(self, credentials: dict) -> None:
        self.credentials = credentials

    @property
    def access_token(self) -> str:
        assert self.credentials, 'required to set credentials with "VKCredentials.set(CRED_DATA)"'

        return self.credentials.get(vk_const.ACCESS_TOKEN)

    @property
    def api_version(self) -> str:
        assert self.credentials, 'required to set credentials with "VKCredentials.set(CRED_DATA)"'

        return self.credentials.get(vk_const.API_VERSION, DEFAULT_API_VERSION)

    @property
    def lang(self) -> str:
        assert self.credentials, 'required to set credentials with "VKCredentials.set(CRED_DATA)"'

        return self.credentials.get(vk_const.LANG)


# singleton параметры доступа к vk api
VKCredentials = ApiCredentials()


class VK:
    def __init__(self, **kwargs: VKCredentialsData) -> None:
        self.credentials = ApiCredentials(**kwargs)
