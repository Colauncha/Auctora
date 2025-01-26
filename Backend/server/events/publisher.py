import json
from asyncio import run
from server.config import redis_store


async def local_publish(channel: str, data: dict[str, any]):
    redis = await redis_store.get_async_redis()
    data = json.dumps(data)
    await redis.publish(channel, data)


async def publish_otp(data: dict[str, any]):
    await local_publish('OTP-sender', data)


async def publish_reset_token(data: dict[str, any]):
    await local_publish('Reset-token', data)


async def publish_bid_placed(data: dict[str, any]):
    await local_publish('Bid-placed', data)


# if __name__ == '__main__':
#     run(publish_otp(123456))