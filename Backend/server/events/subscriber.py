import logging
from asyncio import run, sleep
import json
from server.config import redis_store
from server.utils.email_context import Emailer

# Configure logging
logging.basicConfig(
    filename='biddius_events.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def send_otp_mail(data):
    logging.info('📨 Sending OTP mail 📫')
    async with Emailer(
        subject='OTP Verification',
        template_name="otp_template.html",
        to=data.get('email'),
        otp=data.get('otp')
    ) as emailer:
        await emailer.send_message()

    logging.info(f'♻ Type: {type(data)} -- {data}')
    logging.info('➡ sent ✅')


async def send_bid_placed_mail(data):
    logging.info('📨 Sending Bid placed mail 📫')
    ...  # some code
    await sleep(0.5)
    logging.info(f'♻ Type: {type(data)} -- {data}')
    logging.info('➡ sent ✅')


async def send_reset_token_mail(data):
    logging.info('📨 Sending Reset token mail 📫')
    async with Emailer(
        subject='Reset Password',
        template_name="reset_token_template.html",
        to=data.get('email'),
        token=data.get('token')
    ) as emailer:
        await emailer.send_message()

    logging.info(f'♻ Type: {type(data)} -- {data}')
    logging.info('➡ sent ✅')


async def send_outbid_mail(data):
    logging.info('📨 Sending Outbid mail 📫')
    ...  # some code
    await sleep(0.5)
    logging.info(f'♻ Type: {type(data)} -- {data}')
    logging.info('➡ sent ✅')


async def send_auction_created_mail(data):
    logging.info('📨 Sending Auction Created mail 📫')
    ...  # some code
    await sleep(0.5)
    logging.info(f'♻ Type: {type(data)} -- {data}')
    logging.info('➡ sent ✅')


async def send_win_auction_mail(data):
    logging.info('📨 Sending Auction Created mail 📫')
    ...  # some code
    await sleep(0.5)
    logging.info(f'♻ Type: {type(data)} -- {data}')
    logging.info('➡ sent ✅')


async def send_fund_account_mail(data):
    logging.info('📨 Sending Funding account mail 📫')
    async with Emailer(
        subject='Transaction Receipt',
        template_name="funding_account_template.html",
        to=data.get('email'),
        amount=data.get('amount'),
        reference=data.get('reference_id'),
        type=data.get('transaction_type'),
        status=data.get('status'),
    ) as emailer:
        await emailer.send_message()
    await sleep(0.5)
    logging.info(f'♻ Type: {type(data)} -- {data}')
    logging.info('➡ sent ✅')


channels = {
    'OTP-sender': send_otp_mail,
    'Bid-placed': send_bid_placed_mail,
    'Reset-token': send_reset_token_mail,
    'OutBid': send_outbid_mail,
    'Create-Auction': send_auction_created_mail,
    'Win-Auction': send_win_auction_mail,
    'Fund-Account': send_fund_account_mail,
    # 'Withdrawal': send_withdrawal_mail,
}


async def listner():
    redis = await redis_store.get_async_redis()
    sub = redis.pubsub()
    await sub.subscribe(*channels.keys())

    while True:
        message = await sub.get_message(ignore_subscribe_messages=True)
        if message:
            logging.info(f'➡ INFO: {message}')
            channel = message.get('channel')
            data = json.loads(message.get('data'))
            task = channels.get(channel, 'OTP-sender')
            await task(data)
        await sleep(0.2)


if __name__ == '__main__':
    try:
        logging.info("➡ Listening for messages from publishers 📬")
        run(listner())
    except KeyboardInterrupt:
        logging.info("\n➡ Exiting subscriber ⛔")
        exit(0)