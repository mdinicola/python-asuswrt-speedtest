import asyncio
import logging
import sys
import time
import json
from pyasuswrt import AsusWrtError, AsusWrtHttp

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger('asyncio').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

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


async def wait_and_return_speedtest_result(client: AsusWrtHttp, timeout: int = 120, poll_frequency: int = 15):
    pass


def convert_history_to_payload():
    pass


async def run_speedtest():
    pass

asyncio.run(run_speedtest())

