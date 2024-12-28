import logging
import time
import json
from configparser import ConfigParser
from pyasuswrt import AsusWrtError, AsusWrtHttp

logger = logging.getLogger(__name__)

class SpeedTest:
    def __init__(self, config: ConfigParser):
        self._config = config


    async def asus_get_speedtest_history(self, client: AsusWrtHttp):
        history = json.loads(await client._AsusWrtHttp__send_req('ookla_speedtest_get_history()'))
        return history['ookla_speedtest_get_history']


    def parse_speedtest_history(self, history: dict, limit: int):
        return history[:limit]


    async def asus_set_speedtest_start_time(self, client: AsusWrtHttp, start_time: int):
        data = f'ookla_start_time={start_time}'
        # data = {"ookla_start_time": start_time}
        await client._AsusWrtHttp__post(path='set_ookla_speedtest_start_time.cgi', command=data)


    async def asus_start_speedtest(self, client: AsusWrtHttp):
        data_type = ""
        data_id = ""
        data = f'type={data_type}&id={data_id}'
        # data = {"type": data_type, "id": data_id}
        await client._AsusWrtHttp__post(path='ookla_speedtest_exe.cgi', command=data)


    async def asus_get_speedtest_result(self, client: AsusWrtHttp):
        result = json.loads(await client._AsusWrtHttp__send_req('ookla_speedtest_get_result()'))
        return result['ookla_speedtest_get_result']


    async def wait_and_return_speedtest_result(self, client: AsusWrtHttp, timeout: int, poll_frequency: int):
        count = 0
        while(count <= timeout):
            time.sleep(poll_frequency)
            count += poll_frequency
            results = await self.asus_get_speedtest_result(client)
            if len(results > 0):
                latest_result = results[-1]
                if latest_result['type'] == "result":
                    return latest_result
        raise Exception(f'Speedtest did not complete within {timeout} seconds')


    def convert_history_to_payload(self):
        pass


    async def run(self):
        client = AsusWrtHttp(
            self._config.get('asus_router', 'host'), 
            self._config.get('asus_router', 'username'),
            self._config.get('asus_router', 'password'), 
            port = self._config.getint('asus_router', 'port'),
            use_https = self._config.getboolean('asus_router', 'use_https')
        )

        speedtest_history = self.parse_speedtest_history(
            history = await self.asus_get_speedtest_history(client), 
            limit = self._config.getint('speedtest', 'history_limit')
        )

        print(speedtest_history)

        await client.async_disconnect()