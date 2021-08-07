from unittest import TestCase, skip
from unittest.mock import patch

import vk_cli.api.vk_const as vk_const
from tests.credentials import VK_CREDS
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
        }

    @patch('vk_cli.api.vk_request.VKRequest._do_invoke')
    def test_invoke(self, do_invoke):
        do_invoke.return_value = {}
        self.request.invoke()

        self.assertTrue(self.request.is_invoked)
        self.assertIsInstance(self.request.response, VKResponse)

    @patch('vk_cli.api.vk_request.VKRequest._do_invoke')
    def test_invoked(self, do_invoke):
        request2 = self.request.invoked()
        self.assertIs(self.request, request2)
        self.assertTrue(request2.is_invoked)

    @patch('vk_cli.api.vk_request.VKRequest._do_invoke')
    def test_get_invoke_result(self, do_invoke):
        do_invoke.return_value = [{'name': 'Name'}]
        result = self.request.get_invoke_result()

        self.assertTrue(self.request.is_invoked)
        self.assertIsInstance(result, VKResponse)

    @patch('vk_cli.api.vk_request.VKRequest._do_invoke')
    def invoke_response(self, do_invoke):
        do_invoke.return_value = '123'
        request = VKRequest('utils.getServerTime')
        result = request.invoke_response()

        self.assertEqual(result, '123')
        do_invoke.assert_called_once()

    def test_from_request(self):
        new = VKRequest.from_request(self.request)

        self.assertIsInstance(new, VKRequest)
        self.assertNotEqual(new, self.request)

        self.assertEqual(new.method_name, self.request.method_name)
        self.assertDictEqual(new.method_params, self.request.method_params)

    def test_params_empty(self):
        self.assertEqual(self.request.method_params, {})

    def test_params_kwargs(self):
        request = VKRequest(self.TEST_METHOD_NAME, **self.params_dict)
        self.assertEqual(request.method_params, self.params_dict)

    def test_params_dict(self):
        request = VKRequest(self.TEST_METHOD_NAME, self.params_dict)
        self.assertEqual(request.method_params, self.params_dict)

    def test_params_dict_and_kwargs(self):
        request = VKRequest(self.TEST_METHOD_NAME, {'param1': 1, 'param2': 2}, **self.params_dict)
        self.assertEqual(request.method_params, {'param1': 1, 'param2': 2, **self.params_dict})

    def test_set_param(self):
        params_count_before = len(self.request.method_params)
        self.request.set_param('test', 'value')

        self.assertEqual(len(self.request.method_params), params_count_before + 1)
        self.assertIn('test', self.request.method_params)
        self.assertEqual(self.request.method_params.get('test'), 'value')

    def test_get_prepared_parameters(self):
        request = VKRequest(self.TEST_METHOD_NAME, **self.params_dict)
        prepared = request._prepared_parameters()

        self.assertIn(vk_const.ACCESS_TOKEN, prepared)
        self.assertIn(vk_const.API_VERSION, prepared)
        self.assertIn(vk_const.HTTPS, prepared)

        for key in self.params_dict.keys():
            self.assertIn(key, prepared)

    @skip('skipping')
    def test_captcha(self):
        r = VKRequest('captcha.force')
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
