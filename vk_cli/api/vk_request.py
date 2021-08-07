import logging

import requests

from . import vk_const
from .misc import timer, get_model_class
from .vk_api_error import VKApiErrorFactory, VKApiError, VKApiAccessError
from .vk_credentials import VKCredentials
from .vk_response import VKResponse

log = logging.getLogger(__name__)


class VKRequest:
    attempts = 1  # By default there is 1 attempt for loading
    method_params = {}
    method_params_prepared = None

    credentials = VKCredentials

    def __init__(self, method_name, parameters=None, **pars):
        self.method_name = method_name
        self.method_params = parameters or self.method_params
        self.method_params = {**self.method_params, **pars}

        self.response = None
        self.binded_model = None

    @classmethod
    def from_request(cls, request):
        pre = cls(method_name=None)
        pre._init_from_request(request)
        return pre

    def _init_from_request(self, request):
        from copy import deepcopy
        self.__dict__ = deepcopy(request.__dict__)

    def __str__(self) -> str:
        inv = ('stub', 'invoked')[self.is_invoked]
        binding = ''
        if self.binded_model:
            binding = f'--> \'{self.binded_model.__name__}\''
        return f'{self.method_name}({self.method_params}) [{inv}] {binding}'

    @property
    def is_binded(self):
        return self.binded_model is not None

    @property
    def is_invoked(self):
        return self.response is not None

    def set_param(self, param, value):
        self.method_params[param] = value

    def _prepared_parameters(self):
        if self.method_params_prepared is None:
            self.method_params_prepared = self.method_params.copy()

            token = self.credentials.access_token

            if token is not None:
                self.method_params_prepared[vk_const.ACCESS_TOKEN] = token

            # Set actual version of API
            self.method_params_prepared[vk_const.API_VERSION] = self.credentials.api_version

            # Set preferred language for request
            # self.mPreparedParameters.add(VKApiConst.LANG, getLang())

            # If request is secure, we need all urls as https
            self.method_params_prepared[vk_const.HTTPS] = "1"

            # if token is not None & token.secret is not None:
            # # If it not, generate signature of request
            # sig = generateSig(token)
            # self.mPreparedParameters.add('sig', sig)  # VKApiConst.SIG, sig

            # From that moment you cannot modify parameters.
            # Specially for http loading

        return self.method_params_prepared

    def invoke(self):
        """
        Выполнение запроса, формирование и сохранение результата
        """
        raw_result = self._do_invoke()
        assert raw_result is not None

        self.response = VKResponse(self, raw_result)

    def invoked(self):
        if not self.is_invoked:
            self.invoke()
        return self

    @timer
    def _do_invoke(self):
        """
        Непосредственный вызов одного из методов API vk.com
        """
        log.debug('_do_invoke')
        log.info(f'* {self.method_name}: {self.method_params}')

        params = self.method_params

        for k, w in params.items():  # cast params
            if isinstance(w, bool):
                params[k] = int(w)
            elif isinstance(w, list) or isinstance(w, set):
                params[k] = ','.join(map(str, w))

        self.method_params = {k: v for k, v in params.items() if v is not None}

        str_params = {}
        prepared = self._prepared_parameters()

        for k, v in prepared.items():
            str_params[k] = str(v).encode('utf-8')

        url = 'https://api.vk.com/method/' + self.method_name
        while True:
            try:
                resp = requests.post(url, data=str_params)
                resp.raise_for_status()

                json_resp = resp.json()
                try:
                    return json_resp['response']
                except KeyError:
                    raise VKApiErrorFactory.get_exception(json_resp.get('error') or json_resp)

            except VKApiError as e:
                if e.code in (6, 10):  # если запросы отправляются слишком часто
                    import time
                    # time.sleep(.33)
                    log.exception(e)
                    log.info('sleep for 1 sec')
                    time.sleep(1)

                elif e.code == 14:  # требуется ввод кода с картинки
                    captha_r = VKCapchaR(e.error['captcha_sid'], e.error['captcha_img'], self.method_name, **params)
                    captha_r.show()
                    captha_r.get_input()
                    rr = captha_r.invoke_response(self.method_name, self.secure, **params)
                    return rr

                elif e.code in (7, 15):  # доступ запрещён
                    raise VKApiAccessError(e)

                else:
                    # logger_api.error(name, extra={'dict': pformat(response)})
                    raise

    def invoke_response(self):
        return self._do_invoke()

    def get_invoke_result(self, update=False):
        """
        Результат выполнения запроса
        :return:
        """
        if not self.is_invoked or update:
            self.invoke()
        return self.response

    def bind_model(self, model_class_name):
        """
        Сопоставление запросу модели по имени класса
        :param model_class_name:
        :return:
        """
        self.binded_model = get_model_class(model_class_name)


class PartialRequest(VKRequest):
    offset = None
    count = None

    def __init__(self, request, step, offset):
        super().__init__(None)
        self._init_from_request(request)
        # self.response = None

        self.set_offset(offset)
        self.set_count(step)

    def set_offset(self, offset):
        self.offset = offset

        old_offset = self.method_params.get('offset', 0)
        if self.offset != old_offset:
            self.set_param('offset', offset)
            self.response = None

    def set_count(self, step):
        self.count = step

        old_count = self.method_params.get('count', 0)
        if self.count != old_count:
            self.set_param('count', self.count)
            self.response = None

    def __str__(self):
        if self.is_invoked:
            res = f' [{self.response.count} items]'
        else:
            res = ''
        return f'{self.method_name}: {self.method_params} \ninvoked = {self.is_invoked}{res}'
