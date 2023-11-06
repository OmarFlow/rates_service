import json
import logging

from redis import asyncio as aioredis
from fastapi import FastAPI

from utils import db_request, build_response, switch_exchanger

app = FastAPI()


@app.get("/courses")
async def root(symbol: str = 'btcrub', exchanger: str = "binance"):
    upper_symbol = f"'{symbol.upper()}'"
    exchanger = f"'{exchanger}'"
    redis_key = f"{symbol}{exchanger}"

    redis = await aioredis.from_url("redis://redis:6379", decode_responses=True)

    redis_response = await redis.get(redis_key)
    if redis_response:
        logging.debug(f"Get {redis_key} from redis")
        await redis.close()
        return json.loads(redis_response)

    db_response = await db_request(exchanger, upper_symbol)
    if db_response:
        value = db_response[0][0]
        if value == 'unavailable':
            exchanger = switch_exchanger(exchanger)
            db_response = await db_request(exchanger, upper_symbol)
            value = db_response[0][0]
            if value == 'unavailable':
                logging.critical("All exchangers are down")
                await redis.close()
                return {"error": "exchangers are down"}
            response = build_response(value, exchanger, upper_symbol)
            await redis.set(redis_key, json.dumps(response), ex=3)
            logging.debug(f"Set {redis_key} to redis")
            await redis.close()
            return response
        else:
            response = build_response(value, exchanger, upper_symbol)
            await redis.set(redis_key, json.dumps(response), ex=3)
            logging.debug(f"Set {redis_key} to redis")
            await redis.close()
            return response
    await redis.close()
    logging.error('Invalid symbols')
    return {"error": "not allowed symbols"}