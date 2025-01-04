import logging
import time
import json
import urllib.parse
from configparser import ConfigParser
from pyasuswrt import AsusWrtHttp

logger = logging.getLogger(__name__)


class SpeedtestClient:
    def __init__(self, config: ConfigParser):
        self._config = config
        self._asuswrt_client = AsusWrtHttp(
            self._config.get('asus_router', 'host'),
            self._config.get('asus_router', 'username'),
            self._config.get('asus_router', 'password'),
            port=self._config.getint('asus_router', 'port'),
            use_https=self._config.getboolean('asus_router', 'use_https')
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self._asuswrt_client is not None:
            await self._asuswrt_client.async_disconnect()

    async def asus_get_speedtest_history(self):
        history = json.loads(await self._asuswrt_client._AsusWrtHttp__send_req('ookla_speedtest_get_history()'))
        return history['ookla_speedtest_get_history']

    def parse_speedtest_history(self, history: dict, limit: int):
        return history[:limit]

    async def asus_set_speedtest_start_time(self, start_time: int):
        data = f'ookla_start_time={start_time}'
        # data = {"ookla_start_time": start_time}
        await self._asuswrt_client._AsusWrtHttp__post(path='set_ookla_speedtest_start_time.cgi', command=data)

    async def asus_start_speedtest(self):
        data_type = ""
        data_id = ""
        data = f'type={data_type}&id={data_id}'
        # data = {"type": data_type, "id": data_id}
        await self._asuswrt_client._AsusWrtHttp__post(path='ookla_speedtest_exe.cgi', command=data)

    async def asus_get_speedtest_result(self):
        result = json.loads(await self._asuswrt_client._AsusWrtHttp__send_req('ookla_speedtest_get_result()'))
        return result['ookla_speedtest_get_result']

    async def wait_and_return_speedtest_result(self, timeout: int, poll_frequency: int):
        count = 0
        while (count <= timeout):
            time.sleep(poll_frequency)
            count += poll_frequency
            results = await self.asus_get_speedtest_result()
            if len(results) > 1:
                x = -1
                if len(results[x]) == 0:
                    x = -2
                latest_result = results[x]
                if latest_result['type'] == "result":
                    return latest_result
        raise Exception(f'Speedtest did not complete within {timeout} seconds')

    def convert_history_to_request_payload(self, history: dict):
        payload = ""
        for record in history:
            if len(record) > 0:
                payload += json.dumps(record, separators=(',', ':')) + '\n'
        return urllib.parse.quote_plus(payload)

    async def asus_write_speedtest_history(self, history: str):
        data = f'speedTest_history={history}'
        await self._asuswrt_client._AsusWrtHttp__post(path='ookla_speedtest_write_history.cgi', command=data)

    async def save_speedtest_results(self, result: dict, history_limit: int):
        history = self.parse_speedtest_history(await self.asus_get_speedtest_history(), history_limit)
        history.insert(0, result)
        payload = self.convert_history_to_request_payload(history)

        error = None
        success = None
        try:
            await self.asus_write_speedtest_history(payload)
            success = True
        except Exception as e:
            success = False
            error = e
        finally:
            return {
                'success': success,
                'data': payload,
                'error': error
            }

    async def run(self):
        timestamp = int(time.time())

        print('Setting speedtest start time')
        await self.asus_set_speedtest_start_time(timestamp)
        print('Setting speedtest start time...complete')

        print(f'Starting speedtest at {timestamp}')
        await self.asus_start_speedtest()

        print('Waiting for speedtest to finish')
        speedtest_result = await self.wait_and_return_speedtest_result(
            timeout=self._config.getint('speedtest', 'timeout'),
            poll_frequency=self._config.getint('speedtest', 'poll_frequency')
        )
        print('Waiting for speedtest to finish...complete')

        print('Saving speedtest result')
        save_result = await self.save_speedtest_results(
            result=speedtest_result,
            history_limit=self._config.getint('speedtest', 'history_limit')
        )
        print('Saving speedtest result...complete')
        print(f'Save successful: {save_result['success']}')
