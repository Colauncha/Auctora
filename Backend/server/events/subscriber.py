import logging
from asyncio import run, sleep
import json
from server.config import redis_store, app_configs
from server.utils.email_context import Emailer
from server.services.misc_service import ContactUsService

# Configure logging
logging.basicConfig(
    filename='/var/log/biddius-logs/biddius_events.log'\
        if app_configs.ENV == 'production' else 'biddius_events.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def send_otp_mail(data):
    logging.info('📨 Sending OTP mail 📫')
    if data.get('email') is None or data.get('otp') is None:
        logging.error('❌ No email or OTP provided in data for OTP mail')
        return
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
    if data.get('email') is None:
        logging.error('❌ No email provided in data for bid placed')
        return
    async with Emailer(
        subject="Bid Placed Successfully",
        template_name="bid_placed_template.html",
        to=data.get("email"),
        user=data.get("user"),
        link=data.get("link"),
        reply_to="support@biddius.com",
    ) as emailer:
        await emailer.send_message()
    await sleep(0.5)
    logging.info(f'♻ Type: {type(data)} -- {data}')
    logging.info('➡ sent ✅')


async def send_reset_token_mail(data):
    logging.info('📨 Sending Reset token mail 📫')
    if data.get('email') is None or data.get('token') is None:
        logging.error('❌ No email or token provided in data for reset token')
        return
    async with Emailer(
        subject="Reset Password",
        template_name="reset_token_template.html",
        to=data.get("email"),
        token=data.get("token"),
    ) as emailer:
        await emailer.send_message()

    logging.info(f'♻ Type: {type(data)} -- {data}')
    logging.info('➡ sent ✅')


async def send_outbid_mail(data):
    logging.info('📨 Sending Outbid mail 📫')
    if data.get('email') is None:
        logging.error('❌ No email provided in data for outbid')
        return
    async with Emailer(
        subject="You Have been Outbid!",
        template_name="outbid_template.html",
        to=data.get("email"),
        link=data.get("link"),
        reply_to="support@biddius.com",
    ) as emailer:
        await emailer.send_message()
    await sleep(0.5)
    logging.info(f'♻ Type: {type(data)} -- {data}')
    logging.info('➡ sent ✅')


async def send_auction_created_mail(data):
    logging.info('📨 Sending Auction Created mail 📫')
    if data.get('email') is None:
        logging.error('❌ No email provided in data for auction creation')
        return
    async with Emailer(
        subject="You Are Invited to Participate in an Auction!",
        template_name="participant_invite_template.html",
        to=data.get("email"),
        link=data.get("link"),
        name=data.get("item")["name"] if data.get("item") else "N/A",
        description=data.get("item")["description"] if data.get("item") else "N/A",
        start_price=(
            data.get("auction")["start_price"] if data.get("auction") else "N/A"
        ),
        current_price=(
            data.get("auction")["current_price"] if data.get("auction") else "N/A"
        ),
        start_date=data.get("auction")["start_date"] if data.get("auction") else "N/A",
        end_date=data.get("auction")["end_date"] if data.get("auction") else "N/A",
        item_image=data.get("item_image") if data.get("item_image") else None,
        auction=data.get("auction"),
        reply_to="support@biddius.com",
    ) as emailer:
        await emailer.send_message()
    await sleep(0.5)
    logging.info(f'♻ Type: {type(data)} -- {data}')
    logging.info('➡ sent ✅')


async def send_win_auction_mail(data):
    logging.info('📨 Sending Win Auction mail 📫')
    if data.get('email') is None:
        logging.error('❌ No email provided in data for winning auction')
        return
    async with Emailer(
        subject="Auction Won",
        template_name="win_auction_template.html",
        to=data.get("email"),
        user=data.get("user"),
        link=data.get("link"),
        reply_to="support@biddius.com",
    ) as emailer:
        await emailer.send_message()
    await sleep(0.5)
    logging.info(f'♻ Type: {type(data)} -- {data}')
    logging.info('➡ sent ✅')


async def send_part_invite_mail(data):
    logging.info('📨 Sending Participant Invite mail 📫')
    if data.get('email') is None:
        logging.error('❌ No email provided in data for participant invite')
        return
    print(f'From subscriber.send_part_invite_mail:\n{data}')
    async with Emailer(
        subject="You Are Invited to Participate in an Auction!",
        template_name="participant_invite_template.html",
        to=data.get("email"),
        link=data.get("link"),
        signup_link=data.get("sign_up_link"),
        name=data.get("item")["name"] if data.get("item") else "N/A",
        description=data.get("item")["description"] if data.get("item") else "N/A",
        start_price=(
            data.get("auction")["start_price"] if data.get("auction") else "N/A"
        ),
        current_price=(
            data.get("auction")["current_price"] if data.get("auction") else "N/A"
        ),
        start_date=data.get("auction")["start_date"] if data.get("auction") else "N/A",
        end_date=data.get("auction")["end_date"] if data.get("auction") else "N/A",
        item_image=data.get("item_image") if data.get("item_image") else None,
        auction=data.get("auction"),
        reply_to="support@biddius.com",
    ) as emailer:
        await emailer.send_message()
    await sleep(0.5)
    logging.info(f'♻ Type: {type(data)} -- {data}')
    logging.info('➡ sent ✅')


async def send_fund_account_mail(data):
    logging.info('📨 Sending Funding account mail 📫')
    if data.get('email') is None:
        logging.error('❌ No email provided in data for funding account')
        return
    async with Emailer(
        subject="Transaction Receipt",
        template_name="funding_account_template.html",
        to=data.get("email"),
        amount=data.get("amount"),
        reference=data.get("reference_id"),
        type=data.get("transaction_type"),
        status=data.get("status"),
        reply_to="support@biddius.com",
    ) as emailer:
        await emailer.send_message()
    await sleep(0.5)
    logging.info(f'♻ Type: {type(data)} -- {data}')
    logging.info('➡ sent ✅')


async def send_withdrawal_mail(data):
    logging.info('📨 Sending Withdrawal Receipt mail 📫')
    if data.get('email') is None:
        logging.error('❌ No email provided in data for withdrawal receipt')
        return
    async with Emailer(
        subject='Withdrawal Receipt',
        template_name="wallet_withdrawal_template.html",
        to=data.get('email'),
        amount=data.get('amount'),
        reference=data.get('reference_id'),
        type=data.get('transaction_type'),
        status=data.get('status'),
        reply_to="support@biddius.com",
    ) as emailer:
        await emailer.send_message()
    await sleep(0.5)
    logging.info(f'♻ Type: {type(data)} -- {data}')
    logging.info('➡ sent ✅')


async def send_contact_us_mail(data):
    logging.info('📨 Sending Contact Us mail 📫')
    await ContactUsService.contact_us(data)
    await sleep(0.5)
    logging.info('➡ sent ✅')


MAX_ATTEMPTS = 3
BASE_BACKOFF = 2  # seconds, doubles each retry (2, 4, 8...)


async def execute_with_retry(task, data, channel):
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            await task(data)
            return
        except Exception as e:
            if attempt >= MAX_ATTEMPTS:
                logging.error(
                    f"💀 Dead letter: channel={channel} failed after "
                    f"{MAX_ATTEMPTS} attempts. Last error: {e}"
                )
                return
            backoff = BASE_BACKOFF**attempt
            logging.warning(
                f"⚠ Attempt {attempt}/{MAX_ATTEMPTS} failed for channel={channel}, "
                f"retrying in {backoff}s. Error: {e}"
            )
            await sleep(backoff)


channels = {
    'OTP-sender': send_otp_mail,
    'Bid-placed': send_bid_placed_mail,
    'Reset-token': send_reset_token_mail,
    'OutBid': send_outbid_mail,
    'Create-Auction': send_auction_created_mail,
    'Win-Auction': send_win_auction_mail,
    'Fund-Account': send_fund_account_mail,
    'Withdrawal': send_withdrawal_mail,
    'Contact-us': send_contact_us_mail,
    'Refund-Req-Buyer': send_contact_us_mail,
    'Refund-Req-Seller': send_contact_us_mail,
    'Participant-Invite': send_part_invite_mail,
}


async def listner():
    redis = await redis_store.get_async_redis()
    sub = redis.pubsub()
    await sub.subscribe(*channels.keys())

    while True:
        try:
            message = await sub.get_message(ignore_subscribe_messages=True)
            if message:
                logging.info(f"➡ INFO: {message}")
                channel = message.get("channel")
                data = json.loads(message.get("data"))
                task = channels.get(channel, "OTP-sender")
                await execute_with_retry(task, data, channel)
            await sleep(0.2)
        except Exception as e:
            logging.error(f"❌ Error processing message: {e}")
            await sleep(1)


if __name__ == '__main__':
    try:
        logging.info("➡ Listening for messages from publishers 📬")
        run(listner())
    except KeyboardInterrupt:
        logging.info("\n➡ Exiting subscriber ⛔")
        exit(0)
