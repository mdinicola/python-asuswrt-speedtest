import pytest
import configparser
import json
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
def mock_latest_speedtest_result():
    with open('tests/fixtures/ookla_speedtest_latest_result.json', 'r') as file:
        yield json.load(file)


@pytest.fixture()
def mock_speedtest_history_payload():
    with open('tests/fixtures/ookla_speedtest_history_payload.txt', 'r') as file:
        yield file.read().strip()


@pytest.fixture()
def mock_speedtest_updated_history_payload():
    with open('tests/fixtures/ookla_speedtest_updated_history_payload.txt', 'r') as file:
        yield file.read().strip()


@pytest.fixture()
def mock_write_speedtest_result():
    with patch.object(AsusWrtHttp, '_AsusWrtHttp__post') as m:
        yield m


@pytest.fixture()
def mock_write_speedtest_result_failure():
    with patch.object(AsusWrtHttp, '_AsusWrtHttp__post') as m:
        m.side_effect = Exception('request failed')
        yield m


@pytest.mark.asyncio
async def test_convert_history_to_request_payload(
    speedtest_client,
    mock_get_speedtest_history,
    mock_speedtest_history_payload
):
    data = await speedtest_client.asus_get_speedtest_history()
    payload = speedtest_client.convert_history_to_request_payload(data)
    assert isinstance(payload, str)
    assert payload == mock_speedtest_history_payload


@pytest.mark.asyncio
async def test_save_speedtest_results(
    speedtest_client,
    mock_get_speedtest_history,
    mock_write_speedtest_result,
    mock_latest_speedtest_result,
    mock_speedtest_updated_history_payload
):
    history_limit = 10
    result = await speedtest_client.save_speedtest_results(mock_latest_speedtest_result, history_limit)
    assert isinstance(result, dict)
    assert result['success'] == True
    assert result['error'] is None
    assert result['data'] == mock_speedtest_updated_history_payload


@pytest.mark.asyncio
async def test_save_speedtest_results_failure(
    speedtest_client,
    mock_get_speedtest_history,
    mock_write_speedtest_result_failure,
    mock_latest_speedtest_result,
    mock_speedtest_updated_history_payload
):
    history_limit = 10
    result = await speedtest_client.save_speedtest_results(mock_latest_speedtest_result, history_limit)
    assert isinstance(result, dict)
    assert result['success'] == False
    assert result['error'] is not None
    assert result['data'] is not None
