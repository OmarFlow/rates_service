import logging
from os import getenv


import aio_pika
from dotenv import load_dotenv

load_dotenv()
user = getenv('RABBIT_USER')
password = getenv('RABBIT_PASSWORD')


async def to_writer(symbols: str) -> None:
    connection = await aio_pika.connect_robust(
        f"amqp://{user}:{password}@rabbit:5672/",
    )
    logging.info("Sending to writer")
    async with connection:
        routing_key = "to_write_currency"

        channel = await connection.channel()

        await channel.default_exchange.publish(
            aio_pika.Message(body=symbols.encode()),
            routing_key=routing_key,
        )
