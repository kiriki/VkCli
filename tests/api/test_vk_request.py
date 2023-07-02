from unittest.mock import patch

import pytest

from tests.credentials import VK_CREDS
from vk_cli.api import vk_const
from vk_cli.api.vk_api_error import VKECaptchaNeeded
from vk_cli.api.vk_credentials import VK
from vk_cli.api.vk_request import VKRequest
from vk_cli.api.vk_response import VKResponse

TEST_METHOD_NAME = 'method_class.method_name'

params_dict = {
    'owner_id': 111,
    'album_id': 222,
    'count': 33,
    'offset': 44,
    'extended': True,
    'none_param': None,
}


@pytest.fixture
def vk() -> VK:
    return VK(**VK_CREDS)


@pytest.fixture
def vk_request(vk: VK) -> VKRequest:
    return VKRequest(vk, 'account.getInfo')


@pytest.fixture
def request_info2(vk: VK) -> VKRequest:  # r0
    return VKRequest(vk, 'account.getInfo', {'https_required': 1})


@pytest.fixture
def request_time(vk: VK) -> VKRequest:
    return VKRequest(vk, 'utils.getServerTime')


def test_invoke(vk_request: VKRequest) -> None:
    with patch('vk_cli.api.vk_request.VKRequest._do_invoke', return_value={}):
        vk_request.invoke()

    assert vk_request.is_invoked
    assert isinstance(vk_request.response, VKResponse)


def test_invoked(vk_request: VKRequest) -> None:
    with patch('vk_cli.api.vk_request.VKRequest._do_invoke', return_value={}):
        request2 = vk_request.invoked()
    assert vk_request is request2
    assert request2.is_invoked


def test_get_invoke_result(vk_request: VKRequest) -> None:
    with patch('vk_cli.api.vk_request.VKRequest._do_invoke', return_value=[{'name': 'Name'}]):
        result = vk_request.get_invoke_result()

    assert vk_request.is_invoked
    assert isinstance(result, VKResponse)


def test_invoke_response(vk: VK) -> None:
    with patch('vk_cli.api.vk_request.VKRequest._do_invoke', return_value='123') as do_invoke:
        request = VKRequest(vk, 'utils.getServerTime')
        result = request.invoke_response()

    assert result == '123'
    do_invoke.assert_called_once()


def test_from_request(vk_request: VKRequest) -> None:
    new = VKRequest.from_request(vk_request)

    assert isinstance(new, VKRequest)
    assert new != vk_request

    assert new.method_name == vk_request.method_name
    assert new.method_params == vk_request.method_params


def test_params_empty(vk_request: VKRequest) -> None:
    assert vk_request.method_params == {}


def test_params_kwargs(vk: VK) -> None:
    request = VKRequest(vk, TEST_METHOD_NAME, **params_dict)
    assert request.method_params == params_dict


def test_params_dict(vk: VK) -> None:
    request = VKRequest(vk, TEST_METHOD_NAME, params_dict)
    assert request.method_params == params_dict


def test_params_dict_and_kwargs(vk: VK) -> None:
    request = VKRequest(vk, TEST_METHOD_NAME, {'param1': 1, 'param2': 2}, **params_dict)
    assert request.method_params == {'param1': 1, 'param2': 2, **params_dict}


def test_set_param(vk_request: VKRequest) -> None:
    params_count_before = len(vk_request.method_params)
    vk_request.set_param('test', 'value')

    assert len(vk_request.method_params) == params_count_before + 1
    assert 'test' in vk_request.method_params
    assert vk_request.method_params.get('test') == 'value'


def test_get_prepared_parameters(vk: VK) -> None:
    request = VKRequest(vk, TEST_METHOD_NAME, **params_dict)
    prepared = request._prepared_parameters

    assert vk_const.ACCESS_TOKEN in prepared
    assert vk_const.API_VERSION in prepared

    for key in params_dict:
        assert key in prepared


@pytest.mark.skip('skipping')
def test_captcha(vk: VK) -> None:
    r = VKRequest(vk, 'captcha.force')
    with pytest.raises(VKECaptchaNeeded):
        r.invoke_response()
