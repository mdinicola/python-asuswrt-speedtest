import asyncio
import logging
import sys
import configparser
from speedtest import SpeedTest

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger('asyncio').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read('../config/config.ini')

speedtest = SpeedTest(config)
asyncio.run(speedtest.run())
