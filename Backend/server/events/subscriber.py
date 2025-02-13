from asyncio import run, sleep
import json
from server.config import redis_store
from server.utils.email_context import Emailer


async def send_otp_mail(data):
    print('📨 Sending OTP mail 📫')
    async with Emailer(
        subject='OTP Verification',
        template_name="otp_template.html",
        to=data.get('email'),
        otp=data.get('otp')
    ) as emailer:
        await emailer.send_message()

    print(f'♻ Type: {type(data)} -- {data}')
    print('➡ sent ✅')


async def send_bid_placed_mail(data):
    print('📨 Sending Bid placed mail 📫')
    ...  # some code
    await sleep(0.5)
    print(f'♻ Type: {type(data)} -- {data}')
    print('➡ sent ✅')


async def send_reset_token_mail(data):
    print('📨 Sending Reset token mail 📫')
    async with Emailer(
        subject='Reset Password',
        template_name="reset_token_template.html",
        to=data.get('email'),
        token=data.get('token')
    ) as emailer:
        await emailer.send_message()

    print(f'♻ Type: {type(data)} -- {data}')
    print('➡ sent ✅')


async def send_outbid_mail(data):
    print('📨 Sending Outbid mail 📫')
    ...  # some code
    await sleep(0.5)
    print(f'♻ Type: {type(data)} -- {data}')
    print('➡ sent ✅')


async def send_auction_created_mail(data):
    print('📨 Sending Auction Created mail 📫')
    ...  # some code
    await sleep(0.5)
    print(f'♻ Type: {type(data)} -- {data}')
    print('➡ sent ✅')


async def send_win_auction_mail(data):
    print('📨 Sending Auction Created mail 📫')
    ...  # some code
    await sleep(0.5)
    print(f'♻ Type: {type(data)} -- {data}')
    print('➡ sent ✅')


channels = {
    'OTP-sender': send_otp_mail,
    'Bid-placed': send_bid_placed_mail,
    'Reset-token': send_reset_token_mail,
    'OutBid': send_outbid_mail,
    'Create-Auction': send_auction_created_mail,
    'Win-Auction': send_win_auction_mail,
}


async def listner():
    redis = await redis_store.get_async_redis()
    sub = redis.pubsub()
    await sub.subscribe(*channels.keys())

    while True:
        message = await sub.get_message(ignore_subscribe_messages=True)
        if message:
            print(f'➡ INFO: {message}')
            channel = message.get('channel')
            data = json.loads(message.get('data'))
            task = channels.get(channel, 'OTP-sender')
            await task(data)
        await sleep(0.2)



if __name__ == '__main__':
    try:
        print("➡ Listening for messages from publishers 📬")
        run(listner())
    except KeyboardInterrupt:
        print("\n➡ Exiting subscriber ⛔")
        exit(0)