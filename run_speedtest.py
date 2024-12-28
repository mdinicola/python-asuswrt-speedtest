import asyncio
import logging
import sys
import time
import json
import configparser
from pyasuswrt import AsusWrtError, AsusWrtHttp

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger('asyncio').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read('config/config.ini')

async def asus_get_speedtest_history(client: AsusWrtHttp):
    history = json.loads(await client._AsusWrtHttp__send_req('ookla_speedtest_get_history()'))
    return history['ookla_speedtest_get_history']


def parse_speedtest_history(history: dict, limit: int):
    return history[:limit]


async def asus_set_speedtest_start_time(client: AsusWrtHttp, start_time: int):
    data = f'ookla_start_time={start_time}'
    # data = {"ookla_start_time": start_time}
    await client._AsusWrtHttp__post(path='set_ookla_speedtest_start_time.cgi', command=data)


async def asus_start_speedtest(client: AsusWrtHttp):
    data_type = ""
    data_id = ""
    data = f'type={data_type}&id={data_id}'
    # data = {"type": data_type, "id": data_id}
    await client._AsusWrtHttp__post(path='ookla_speedtest_exe.cgi', command=data)


async def asus_get_speedtest_result(client: AsusWrtHttp):
    result = json.loads(await client._AsusWrtHttp__send_req('ookla_speedtest_get_result()'))
    return result['ookla_speedtest_get_result']


async def wait_and_return_speedtest_result(client: AsusWrtHttp, timeout: int, poll_frequency: int):
    count = 0
    while(count <= timeout):
        time.sleep(poll_frequency)
        count += poll_frequency
        results = await asus_get_speedtest_result(client)
        if len(results > 0):
            latest_result = results[-1]
            if latest_result['type'] == "result":
                return latest_result
    raise Exception(f'Speedtest did not complete within {timeout} seconds')


def convert_history_to_payload():
    pass


async def run_speedtest():
    client = AsusWrtHttp(
        config.get('asus_router', 'host'), 
        config.get('asus_router', 'username'),
        config.get('asus_router', 'password'), 
        port = config.getint('asus_router', 'port'),
        use_https = config.getboolean('asus_router', 'use_https')
    )

    speedtest_history = parse_speedtest_history(
        history = await asus_get_speedtest_history(client), 
        limit = config.getint('speedtest', 'history_limit')
    )

    await client.async_disconnect()

# asyncio.run(run_speedtest())

