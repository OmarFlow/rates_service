import json
import asyncio
import logging
from os import getenv
from asyncio import sleep

import aiohttp
from dotenv import load_dotenv

from currency_rate.utils import to_writer
from currency_rate.binance_ex import symbols_handbook

load_dotenv()


async def coingecko() -> None:
    params = {'x_cg_api_key': getenv('COINGECKO_API_KEY')}
    while True:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get('https://api.coingecko.com/api/v3/exchange_rates', params=params) as resp:
                    resp_text = await resp.text()
                    resp = json.loads(resp_text)
                    rub = str(resp['rates']['rub']['value'])
                    usd = str(resp['rates']['usd']['value'])
                    logging.debug(f"Courses from coingecko {rub=} and {usd=} have been received")
                    usd_record: dict = {
                        "value": usd,
                        "symbol_id": symbols_handbook["BTCUSDT"],
                        "exchanger": "coingecko"
                    }
                    rub_record: dict = {
                        "value": rub,
                        "symbol_id": symbols_handbook["BTCRUB"],
                        "exchanger": "coingecko"
                    }
                    to_write_symbols: str = json.dumps([usd_record, rub_record])

                    async with asyncio.TaskGroup() as tg:
                        tg.create_task(to_writer(to_write_symbols))
                        tg.create_task(sleep(2))

            except ConnectionError as e:
                logging.error(f'It faced an error while retrieve coingecko data: {str(e)}')
                usd_record: dict = {
                    "value": 'unavailable',
                    "symbol_id": symbols_handbook["BTCUSDT"],
                    "exchanger": "coingecko"
                }
                rub_record: dict = {
                    "value": "unavailable",
                    "symbol_id": symbols_handbook["BTCRUB"],
                    "exchanger": "coingecko"
                }
                to_write_symbols: str = json.dumps([usd_record, rub_record])
                async with asyncio.TaskGroup() as tg:
                    tg.create_task(to_writer(to_write_symbols))
                    tg.create_task(sleep(1))