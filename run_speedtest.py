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
    pass


def parse_speedtest_history(history: dict, limit: int):
    pass


async def asus_set_speedtest_start_time(client: AsusWrtHttp, start_time: int):
    pass


async def asus_start_speedtest(client: AsusWrtHttp):
    pass


async def asus_get_speedtest_result(client: AsusWrtHttp):
    pass


async def wait_and_return_speedtest_result(
    client: AsusWrtHttp, 
    timeout: int = config.getint('speedtest', 'default_timeout'), 
    poll_frequency: int = config.getint('speedtest', 'default_poll_frequency')
):
    pass


def convert_history_to_payload():
    pass


async def run_speedtest():
    pass

# asyncio.run(run_speedtest())

