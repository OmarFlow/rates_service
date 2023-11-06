import asyncio

from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

from models.models import Symbol
from models.db import get_session


async def init_symbol_handbook() -> None:
    session = await get_session()

    try:
        async with session() as session:
            async with session.begin():
               await session.execute(
                   insert(Symbol),
                   [
                       {"name": "BTCRUB"},
                       {"name": "BTCUSDT"},
                       {"name": "ETHRUB"},
                       {"name": "ETHUSDT"},
                       {"name": "USDTRUB"},
                   ],
               )
    except IntegrityError:
        return


asyncio.run(init_symbol_handbook())
