import pytest
import configparser
from unittest.mock import patch
from pyasuswrt import AsusWrtHttp
from src.asuswrtspeedtest import SpeedtestClient


@pytest.fixture(scope="module")
def speedtest_client():
    config = configparser.ConfigParser()
    config.read('tests/config.ini')
    return SpeedtestClient(config)


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


@pytest.fixture()
def mock_get_incomplete_speedtest_result():
    with patch.object(AsusWrtHttp, '_AsusWrtHttp__send_req') as m:
        with open('tests/fixtures/ookla_speedtest_get_incomplete_result.json', 'r') as file:
            m.return_value = file.read()
        yield m


@pytest.mark.asyncio
async def test_get_speedtest_history(speedtest_client, mock_get_speedtest_history):
    data = await speedtest_client.asus_get_speedtest_history()
    assert isinstance(data, list)
    assert len(data) == 19


@pytest.mark.asyncio
async def test_parse_speedtest_history(speedtest_client, mock_get_speedtest_history):
    data = await speedtest_client.asus_get_speedtest_history()
    history_limit = 5
    parsed_data = speedtest_client.parse_speedtest_history(history=data, limit=history_limit)
    assert len(parsed_data) == history_limit


@pytest.mark.asyncio
async def test_get_speedtest_result(speedtest_client, mock_get_speedtest_result):
    data = await speedtest_client.asus_get_speedtest_result()
    assert isinstance(data, list)
    last_result = data[-2]
    assert last_result['type'] == 'result'


@pytest.mark.asyncio
async def test_wait_and_return_speedtest_result(speedtest_client, mock_get_speedtest_result):
    data = await speedtest_client.wait_and_return_speedtest_result(timeout=3, poll_frequency=1)
    assert isinstance(data, dict)
    assert data['type'] == 'result'
    assert data['result']['persisted'] == True


@pytest.mark.asyncio
async def test_wait_and_return_on_speedtest_result_timeout(speedtest_client, mock_get_incomplete_speedtest_result):
    timeout = 2
    poll_frequency = 1
    with pytest.raises(Exception) as excinfo:
        await speedtest_client.wait_and_return_speedtest_result(timeout=timeout, poll_frequency=poll_frequency)
    assert str(excinfo.value) == f'Speedtest did not complete within {timeout} seconds'
