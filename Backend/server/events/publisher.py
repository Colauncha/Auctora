import json
from asyncio import run
from enum import Enum as ENUM
from uuid import UUID as uuid_
from typing import Union

from sqlalchemy import UUID, Enum
from server.config import redis_store


UUID = Union[UUID, uuid_]
ENUM = Union[Enum, ENUM]


async def local_publish(channel: str, data: dict[str, any]):
    redis = await redis_store.get_async_redis()
    data = json.dumps(data)
    await redis.publish(channel, data)

async def dump_data(data: str | dict[str, any]) -> dict[str, any]:
    for k, v in data.items():
        if isinstance(v, ENUM):
            data[k] = v.value
        if isinstance(v, UUID):
            data[k] = str(v)
        if isinstance(v, dict):
            data[k] = await dump_data(v)
    return data


async def publish_otp(data: dict[str, any]):
    data = await dump_data(data)
    await local_publish('OTP-sender', data)


async def publish_reset_token(data: dict[str, any]):
    data = await dump_data(data)
    await local_publish('Reset-token', data)


async def publish_bid_placed(data: dict[str, any]):
    data = await dump_data(data)
    await local_publish('Bid-placed', data)


async def publish_outbid(data: dict[str, any]):
    data = await dump_data(data)
    await local_publish('OutBid', data)


async def publish_create_auction(data: dict[str, any]):
    data = await dump_data(data)
    await local_publish('Create-Auction', data)


async def publish_win_auction(data: dict[str, any]):
    data = await dump_data(data)
    await local_publish('Win-Auction', data)


async def publish_fund_account(data: dict[str, any]):
    # data['transaction_type'] = data['transaction_type'].value
    # data['status'] = data['status'].value
    data = await dump_data(data)
    await local_publish('Fund-Account', data)


# async def publish_withdrawal(data: dict[str, any]):
#     await local_publish('Withdrawal', data)


# if __name__ == '__main__':
#     run(publish_otp(123456))