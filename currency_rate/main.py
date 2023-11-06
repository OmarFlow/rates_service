import logging
import asyncio

from currency_rate.binance_ex import binance
from currency_rate.coingecko_ex import coingecko


async def main() -> None:
    async with asyncio.TaskGroup() as tg:
        tg.create_task(binance())
        tg.create_task(coingecko())

if __name__ == "__main__":
    logging.info("courses retrieval has started")
    asyncio.run(main())
