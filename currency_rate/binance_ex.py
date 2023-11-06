import json
import asyncio
import logging
from os import getenv
from asyncio import sleep

from sqlalchemy import select
from dotenv import load_dotenv
from binance.websocket.spot.websocket_api import SpotWebsocketAPIClient


from models.models import Symbol
from models.db import get_session
from currency_rate.utils import to_writer

load_dotenv()


async def get_symbol_handbook():
    session = await get_session()
    async with session() as session:
        async with session.begin():
            return await session.execute(
                select(Symbol.name, Symbol.id)
            )

loop = asyncio.new_event_loop()
raw_symbol_handbook: tuple[tuple] = tuple(loop.run_until_complete(get_symbol_handbook()))
symbols_handbook: dict[str:int] = {symbol[0]: symbol[1] for symbol in raw_symbol_handbook}


async def symbols_transform(symbols: list[str]) -> str:
    logging.info("Transforming symbols to send to writer")
    transformed_symbols: list[dict] = []
    if symbols:
        for symbol in symbols:
            symbol_result = json.loads(symbol)['result']
            transformed_symbols.append(
                {
                    'value': symbol_result['price'],
                    "symbol_id": symbols_handbook[symbol_result['symbol']],
                    "exchanger": "binance"
                }
            )
    else:
        for symbol_id in symbols_handbook.values():
            transformed_symbols.append(
                {
                    'value': "unavailable",
                    "symbol_id": symbol_id,
                    "exchanger": "binance"
                }
            )
    return json.dumps(transformed_symbols)


async def binance() -> None:
    api_key = getenv("BINANCE_API_KEY")
    api_secret = getenv("BINANCE_API_SECRET")

    symbols_from_binance: list[str] = []

    def message_handler(_, message):
        logging.debug(f"Courses from binance //{message}// have been  received")
        symbols_from_binance.append(message)

    while True:
        try:
            my_client = SpotWebsocketAPIClient(
                'wss://ws-api.binance.com:443/ws-api/v3',
                api_key=api_key,
                api_secret=api_secret,
                on_message=message_handler
            )

            my_client.ticker_price(symbol="BTCRUB")
            my_client.ticker_price(symbol="BTCUSDT")
            my_client.ticker_price(symbol="ETHRUB")
            my_client.ticker_price(symbol="ETHUSDT")
            my_client.ticker_price(symbol="USDTRUB")

            await sleep(1)
            symbols = await symbols_transform(symbols_from_binance)

            my_client.stop()

            async with asyncio.TaskGroup() as tg:
                tg.create_task(sleep(0.7))
                tg.create_task(to_writer(symbols))

            symbols_from_binance.clear()
        except ConnectionError as e:
            logging.error(f'It faced an error while retrieve binance data: {str(e)}')
            symbols = await symbols_transform(symbols_from_binance)
            async with asyncio.TaskGroup() as tg:
                tg.create_task(to_writer(symbols))
                tg.create_task(sleep(1))