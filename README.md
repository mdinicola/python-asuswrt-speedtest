# python-asuswrt-speedtest

Programatically run internet speedtests on your AsusWRT-powered routers.

It uses the [pyasuswrt](https://github.com/ollo69/pyasuswrt) package to make http(s) requests to the router.

Confirmed to be working with AsusWRTMerlin.  It should work for other AsusWRT-powered routers with the Internet Spedtest function available, but this has not been tested.  Use at your own risk.

## Usage

### Config

Configuration is stored in the config/config.ini file.

        [asus_router]
        host = 
        port = 8443
        use_https = true
        username = 
        password = 

        [speedtest]
        timeout = 120
        poll_frequency = 15
        history_limit = 10

### Script

The following will run a speedtest on your router.  The results will be available on the Internet Speed page

1. Clone the repository
2. Copy config/config.example.ini to config/config.ini
3. Update the config/config.ini file with your router credentials and desired settings
4. Run ```python3 ./run_speedtest.py```

### Package

The latest package release is available on PyPI

    pip install asuswrtspeedtest

Example of how to use this package in your own project:

    import asyncio
    import configparser
    from asuswrtspeedtest import SpeedtestClient


    config = configparser.ConfigParser()
    config.read('config/config.ini')


    async def run_speedtest():
        async with SpeedtestClient(config) as speedtest_client:
            await speedtest_client.run()

    asyncio.run(run_speedtest())