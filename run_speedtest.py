import asyncio
import logging
import sys
import configparser
from src.speedtest import SpeedTest

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger('asyncio').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read('config/config.ini')


async def run_speedtest():
    async with SpeedTest(config) as speedtest:
        await speedtest.run()

asyncio.run(run_speedtest())
