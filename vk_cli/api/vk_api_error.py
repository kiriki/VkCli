class VKError(Exception):
    __slots__ = ['error']

    def __init__(self, error_data) -> None:
        self.error = error_data
        super().__init__(self, str(self))

    @property
    def code(self):
        return self.error['error_code']

    @property
    def description(self):
        return self.error['error_msg']

    @property
    def params(self):
        pars = {a['key']: a['value'] for a in self.error['request_params']}
        return pars

    def __str__(self):
        return f"Error(code = '{self.code}', description = '{self.description}', params = '{self.params}')"


class VKEAccessError(VKError):
    def __init__(self, error_data) -> None:
        if isinstance(error_data, VKError):
            super().__init__(error_data.error)
        else:
            super().__init__(error_data)

    def __str__(self):
        return f"[{self.code}] {self.description} params = '{self.params}'"


class VKEInvalidUserId(VKError):
    pass


class VKECaptchaNeeded(VKError):
    pass


class VKETooFrequent(VKError):
    pass


class VKEInternal(VKError):
    pass


class VKApiErrorFactory:
    errors = {
        113: VKEInvalidUserId,
        14: VKECaptchaNeeded,
        6: VKETooFrequent,
        7: VKEAccessError,
        15: VKEAccessError,
    }

    @classmethod
    def get_exception(cls, data):
        exception_cls = cls.errors.get(data['error_code'], VKError)
        return exception_cls(data)  # default
