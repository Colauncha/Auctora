from datetime import datetime
import json
from typing import Union
from asyncio import run
from enum import Enum as PyEnum
from uuid import UUID as PyUUID

from sqlalchemy import UUID as SAUUID, Enum as SAEnum
from server.config import redis_store
from server.models.base import BaseModel


UUIDType = Union[PyUUID, SAUUID]
EnumType = Union[PyEnum, SAEnum]


async def local_publish(channel: str, data: dict[str, any]):
    redis = await redis_store.get_async_redis()
    payload = json.dumps(data)
    await redis.publish(channel, payload)


async def dump_data(data: str | dict[str, any]) -> dict[str, any]:
    for key, value in data.items():
        if isinstance(value, EnumType):
            data[key] = value.value
        elif isinstance(value, UUIDType):
            data[key] = str(value)
        elif isinstance(value, dict):
            data[key] = await dump_data(value)
        elif isinstance(value, BaseModel) or hasattr(value, "to_dict"):
            data[key] = await dump_data(value.to_dict())
        elif isinstance(value, list):
            data[key] = [
                await dump_data(item) if isinstance(item, dict)
                else str(item) if isinstance(item, UUIDType)
                else item for item in value
            ]
        elif isinstance(value, datetime):
            data[key] = value.isoformat()
    return data


async def publish_event(channel: str, data: dict[str, any]):
    processed_data = await dump_data(data)
    await local_publish(channel, processed_data)


# Specific event publishers
async def publish_otp(data: dict[str, any]):
    await publish_event('OTP-sender', data)

async def publish_reset_token(data: dict[str, any]):
    await publish_event('Reset-token', data)

async def publish_bid_placed(data: dict[str, any]):
    await publish_event('Bid-placed', data)

async def publish_outbid(data: dict[str, any]):
    await publish_event('OutBid', data)

async def publish_create_auction(data: dict[str, any]):
    await publish_event('Create-Auction', data)

async def publish_win_auction(data: dict[str, any]):
    await publish_event('Win-Auction', data)

async def publish_fund_account(data: dict[str, any]):
    await publish_event('Fund-Account', data)

async def publish_withdrawal(data: dict[str, any]):
    await publish_event('Withdrawal', data)

async def publish_contact_us(data: dict[str, any]):
    await publish_event('Contact-us', data)

async def publish_refund_req_buyer(data: dict[str, any]):
    await publish_event('Refund-Req-Buyer', data)

async def publish_refund_req_seller(data: dict[str, any]):
    await publish_event('Refund-Req-Seller', data)

async def publish_participant_invite(data: dict[str, any]):
    await publish_event('Participant-Invite', data)