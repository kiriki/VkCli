class VKApiError(Exception):
    __slots__ = ['error']

    def __init__(self, error_data):
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


class VKApiAccessError(VKApiError):
    def __init__(self, error_data):
        if isinstance(error_data, VKApiError):
            super().__init__(error_data.error)
        else:
            super().__init__(error_data)

    def __str__(self):
        return f'[{self.code}] {self.description} params = \'{self.params}\''


class VKApiInvalidUserId(VKApiError):
    pass


class VKApiErrorFactory:
    errors = {
        113: VKApiInvalidUserId
    }

    @classmethod
    def get_exception(cls, data):
        exception_cls = cls.errors.get(data['error_code'], VKApiError)
        return exception_cls(data)  # default
