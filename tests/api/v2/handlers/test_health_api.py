import pytest
import app

from http import HTTPStatus


@pytest.fixture
def expected_caldera_info(loop, api_v2_client, app_svc):
    return {
        'application': 'CALDERA',
        'plugins': [
            {
                'address': '/plugin/sandcat/gui',
                'description': 'A custom multi-platform RAT',
                'enabled': True,
                'name': 'sandcat'
            },
            {
                'address': 'plugin/ssl/gui',
                'description': 'Run an SSL proxy in front of the server',
                'enabled': False,
                'name': 'ssl'
            }
        ],
        'version': app.get_version()
    }


class TestHealthApi:
    async def test_get_health(self, api_v2_client, api_cookies, expected_caldera_info):
        resp = await api_v2_client.get('/api/v2/health', cookies=api_cookies)
        assert resp.status == HTTPStatus.OK
        output_info = await resp.json()
        assert output_info == expected_caldera_info

    async def test_unauthorized_get_health(self, api_v2_client, expected_caldera_info):
        resp = await api_v2_client.get('/api/v2/health')
        assert resp.status == HTTPStatus.OK
        output_info = await resp.json()
        assert output_info == expected_caldera_info
