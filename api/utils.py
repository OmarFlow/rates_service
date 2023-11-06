import logging
from typing import Optional

from sqlalchemy import text

from models.db import get_session


async def db_request(exchanger: str, symbol: str) -> Optional[str]:
    session = await get_session()
    async with session() as session:
        async with session.begin():
            res = await session.execute(
                text(f"SELECT sh.value FROM symbol_history as sh"
                     f" join symbol as s on sh.symbol_id=s.id"
                     f" WHERE exchanger={exchanger} and s.name={symbol}"
                     f" order by created desc limit 1")
            )
            logging.debug(f"Db request with args {exchanger=}, {symbol=}")
            return res.all()


def switch_exchanger(exchanger: str) -> str:
    logging.debug(f"Switch exchanger from {exchanger}")
    if exchanger == "'binance'":
        return "'coingecko'"
    return "'binance'"


def build_response(value: str, exchanger: str, symbol: str) -> dict[str:str]:
    logging.debug(f"Build response with args {exchanger=}, {symbol=}")
    return {
        "exchanger": exchanger,
        "courses":
            {
                "direction": symbol,
                "value": value
            }
    }
