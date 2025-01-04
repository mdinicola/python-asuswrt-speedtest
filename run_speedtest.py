import asyncio
import logging
import sys
import configparser
from src.asuswrtspeedtest import SpeedtestClient

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger('asyncio').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read('config/config.ini')


async def run_speedtest():
    async with SpeedtestClient(config) as speedtest_client:
        await speedtest_client.run()

asyncio.run(run_speedtest())
