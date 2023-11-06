import json
import asyncio
import logging
from os import getenv


import aio_pika
from sqlalchemy import insert
from dotenv import load_dotenv

from models.db import get_session
from models.models import SymbolHistory

load_dotenv()
rabbit_user = getenv('RABBIT_USER')
rabbit_password = getenv('RABBIT_PASSWORD')


async def write_db(message: list[dict]) -> None:
    session = await get_session()
    async with session() as session:
        async with session.begin():
            await session.execute(
                insert(SymbolHistory),
                message
            )
            logging.debug(f"Message - {message} has been write to db")


async def consume() -> None:
    connection = await aio_pika.connect_robust(
        f"amqp://{rabbit_user}:{rabbit_password}@rabbit:5672/",
    )

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)

        queue = await channel.declare_queue("to_write_currency", durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    decoded_message = json.loads(message.body.decode())
                    logging.debug(f"Rabbit get message {message} to write to db")
                    await write_db(decoded_message)


if __name__ == "__main__":
    logging.info("courses consuming to write to db has started")
    asyncio.run(consume())