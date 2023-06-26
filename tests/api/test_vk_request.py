from unittest import TestCase, skip
from unittest.mock import patch

from tests.credentials import VK_CREDS
from vk_cli.api import vk_const
from vk_cli.api.vk_api_error import VKECaptchaNeeded
from vk_cli.api.vk_credentials import VKCredentials
from vk_cli.api.vk_request import VKRequest
from vk_cli.api.vk_response import VKResponse

VKCredentials.set(VK_CREDS)


class TestVKRequest(TestCase):
    def setUp(self):
        self.TEST_METHOD_NAME = 'method_class.method_name'

        self.request = VKRequest('account.getInfo')

        self.r0 = VKRequest('account.getInfo', {'https_required': 1})
        self.r1 = VKRequest('utils.getServerTime')

        self.params_dict = {
            'owner_id': 111,
            'album_id': 222,
            'count': 33,
            'offset': 44,
            'extended': True,
            'none_param': None,
        }

    @patch('vk_cli.api.vk_request.VKRequest._do_invoke')
    def test_invoke(self, do_invoke):
        do_invoke.return_value = {}
        self.request.invoke()

        assert self.request.is_invoked
        assert isinstance(self.request.response, VKResponse)

    @patch('vk_cli.api.vk_request.VKRequest._do_invoke')
    def test_invoked(self, do_invoke):
        request2 = self.request.invoked()
        assert self.request is request2
        assert request2.is_invoked

    @patch('vk_cli.api.vk_request.VKRequest._do_invoke')
    def test_get_invoke_result(self, do_invoke):
        do_invoke.return_value = [{'name': 'Name'}]
        result = self.request.get_invoke_result()

        assert self.request.is_invoked
        assert isinstance(result, VKResponse)

    @patch('vk_cli.api.vk_request.VKRequest._do_invoke')
    def invoke_response(self, do_invoke):
        do_invoke.return_value = '123'
        request = VKRequest('utils.getServerTime')
        result = request.invoke_response()

        assert result == '123'
        do_invoke.assert_called_once()

    def test_from_request(self):
        new = VKRequest.from_request(self.request)

        assert isinstance(new, VKRequest)
        assert new != self.request

        assert new.method_name == self.request.method_name
        self.assertDictEqual(new.method_params, self.request.method_params)

    def test_params_empty(self):
        assert self.request.method_params == {}

    def test_params_kwargs(self):
        request = VKRequest(self.TEST_METHOD_NAME, **self.params_dict)
        assert request.method_params == self.params_dict

    def test_params_dict(self):
        request = VKRequest(self.TEST_METHOD_NAME, self.params_dict)
        assert request.method_params == self.params_dict

    def test_params_dict_and_kwargs(self):
        request = VKRequest(self.TEST_METHOD_NAME, {'param1': 1, 'param2': 2}, **self.params_dict)
        assert request.method_params == {'param1': 1, 'param2': 2, **self.params_dict}

    def test_set_param(self):
        params_count_before = len(self.request.method_params)
        self.request.set_param('test', 'value')

        assert len(self.request.method_params) == params_count_before + 1
        assert 'test' in self.request.method_params
        assert self.request.method_params.get('test') == 'value'

    def test_get_prepared_parameters(self):
        request = VKRequest(self.TEST_METHOD_NAME, **self.params_dict)
        prepared = request._prepared_parameters

        assert vk_const.ACCESS_TOKEN in prepared
        assert vk_const.API_VERSION in prepared

        for key in self.params_dict:
            assert key in prepared

    @skip('skipping')
    def test_captcha(self):
        r = VKRequest('captcha.force')
        with self.assertRaises(VKECaptchaNeeded):
            r.invoke_response()

    @skip('skipping')
    @patch('vk_cli.api.vk_request.VKRequest._do_invoke')
    def test_invoke1(self, _do_invoke):
        _do_invoke.return_value = [{'last_name': 'Дуров'}]

        request = VKRequest('users.get', uids='1,2', fields='education')
        res = request.invoke_response()
        print(res)

        _do_invoke.assert_called_once_with('users.get', uids='1,5', fields='education')

    @skip('skipping')
    def test_invoke2(self):
        params = {'user_ids': '1,5,10'}
        rr = VKRequest('users.get', **params).invoke_response()
        print(rr)
