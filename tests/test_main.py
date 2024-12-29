import pytest
import configparser
from unittest.mock import patch
from src.speedtest import SpeedTest
from pyasuswrt import AsusWrtHttp

@pytest.fixture(scope="module")
def speedtest_client():
    config = configparser.ConfigParser()
    config.read('tests/config.ini')
    return SpeedTest(config)

@pytest.fixture()
def mock_get_speedtest_history():
    with patch.object(AsusWrtHttp, '_AsusWrtHttp__send_req') as m:
        with open('tests/fixtures/ookla_speedtest_get_history.json', 'r') as file:
            m.return_value = file.read()
        yield m

@pytest.fixture()
def mock_get_speedtest_result():
    with patch.object(AsusWrtHttp, '_AsusWrtHttp__send_req') as m:
        with open('tests/fixtures/ookla_speedtest_get_result.json', 'r') as file:
            m.return_value = file.read()
        yield m

@pytest.mark.asyncio
async def test_get_speedtest_history(speedtest_client, mock_get_speedtest_history):
    data = await speedtest_client.asus_get_speedtest_history()
    assert isinstance(data, list)
    assert len(data) == 20

@pytest.mark.asyncio
async def test_parse_speedtest_result(speedtest_client, mock_get_speedtest_history):
    data = await speedtest_client.asus_get_speedtest_history()
    parsed_data = speedtest_client.parse_speedtest_history(history=data, limit=5)
    assert len(parsed_data) == 5

@pytest.mark.asyncio
async def test_get_speedtest_result(speedtest_client, mock_get_speedtest_result):
    data = await speedtest_client.asus_get_speedtest_result()
    assert isinstance(data, list)
    last_result = data[-2]
    assert last_result['type'] == 'result'

@pytest.mark.asyncio
async def test_wait_and_return_speedtest_result(speedtest_client, mock_get_speedtest_result):
    data = await speedtest_client.wait_and_return_speedtest_result(timeout=10, poll_frequency=3)
    assert isinstance(data, dict)
    assert data['type'] == 'result'
    assert data['result']['persisted'] == True