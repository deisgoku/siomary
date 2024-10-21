import logging
import os
import re
import telebot
from telebot import TeleBot
from telebot.types import Update, WebAppInfo, Message
from telebot.util import quick_markup

BOT_TOKEN=os.getenv('BOT_TOKEN')
PAYMENT_PROVIDER_TOKEN=os.getenv('PAYMENT_PROVIDER_TOKEN')
WEBHOOK_URL=os.getenv('WEBHOOK_URL')
WEBHOOK_PATH='/bot'
APP_URL=os.getenv('APP_URL')

bot = TeleBot(BOT_TOKEN, parse_mode=None)

@bot.message_handler(content_types=['successful_payment'])
def handle_successful_payment(message):
    """Message handler for messages containing 'successful_payment' field.
      This message is sent when the payment is successful and the payment flow is done.
      It's a good place to send the user a purchased item (if it is an electronic item, such as a key) 
      or to send a message that an item is on its way.

      The message param doesn't contain info about ordered good - they should be stored separately.
      Find more info: https://core.telegram.org/bots/api#successfulpayment.

      Example of Successful Payment message:
        {
            "update_id":12345,
            "message":{
                "message_id":12345,
                "date":1441645532,
                "chat":{
                    "last_name":"Doe",
                    "id":123456789,
                    "first_name":"John",
                    "username":"johndoe",
                    "type": ""
                },
                "successful_payment": {
                    "currency": "USD",
                    "total_amount": 1000,
                    "invoice_payload": "order_id",
                    "telegram_payment_charge_id": "12345",
                    "provider_payment_charge_id": "12345",
                    "order_info": {
                        "name": "John"
                    }
                }
            }
        }
    """
    user_name = message.successful_payment.order_info.name
    text = f'Makasih udah order, *{user_name}*! Ini adalah kafe hayalan , jadi uangmu aman gak kena cas atau gak kena bayar.\n\nHave a nice day 🙂'
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        parse_mode='markdown'
    )

@bot.pre_checkout_query_handler(func=lambda _: True)
def handle_pre_checkout_query(pre_checkout_query):
    """Here we may check if ordered items are still available.
      Since this is an example project, all the items are always in stock, so we answer query is OK.
      For other cases, when you perform a check and find out that you can't sell the items,
      you need to answer ok=False.
      Keep in mind: The check operation should not be longer than 10 seconds. If the Telegram API
      doesn't receive answer in 10 seconds, it cancels checkout.
    """
    bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id, ok=True)

@bot.message_handler(func=lambda message: re.match(r'/?start', message.text, re.IGNORECASE) is not None)
def handle_start_command(message):
    """Message handler for start messages, including '/start' command. This is an example how to
      use Regex for handling desired type of message. E.g. this handlers applies '/start', 
      '/START', 'start', 'START', 'sTaRt' and so on.
    """
    send_actionable_message(
        chat_id=message.chat.id,
        text='*Welcome to Siomary CAFE* 🏚 \n\n Ini waktunya memesan sesuatu yang enak enak 😋 \n\n Tekan tombol dibawah untuk memulai.'
    )

@bot.message_handler()
def handle_all_messages(message):
    """Fallback message handler that is invoced if none of above aren't match. This is a good
      practice to handle all the messages instead of ignoring unknown ones. In our case, we let user
      know that we can't handle the message and just advice to explore the menu using inline button.
    """
    send_actionable_message(
        chat_id=message.chat.id,
        text="sayangnya abang gak tau harus bales apa , dikarenakan ini bot jadi abang cuma bisa nawarin makanan yang kamu suka 😉"
    )

def send_actionable_message(chat_id, text):
    """Method allows to send the text to the chat and attach inline button to it.
      Inline button will open our Mini App on click.
    """
    markup = quick_markup({
        'Buka List Menu': { 
            'web_app': WebAppInfo(APP_URL)
        },
    }, row_width=1)
    bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode='markdown',
        reply_markup=markup
    )

def refresh_webhook():
    """Just a wrapper for remove & set webhook ops"""
    bot.remove_webhook()
    bot.set_webhook(WEBHOOK_URL + WEBHOOK_PATH)

def process_update(update_json):
    """Pass received Update JSON to the Bot for processing.
      This method should be typically called from the webhook method.
      
    Args:
        update_json: Update object sent from the Telegram API. See https://core.telegram.org/bots/api#update.
    """
    update = Update.de_json(update_json)
    bot.process_new_updates([update])

def create_invoice_link(prices) -> str:
    """Just a handy wrapper for creating an invoice link for payment. Since this is an example project,
      most of the fields are hardcode.
    """
    return bot.create_invoice_link(
        title='Order #1',
        description='Pilihan mantap  👌sekarang waktunya pembayaran 🧭abang nyiapin makanan ',
        payload='orderID',
        provider_token=PAYMENT_PROVIDER_TOKEN,
        currency='IDR',
        prices=prices,
        need_name=True,
        need_phone_number=True,
        need_shipping_address=True
    )

def enable_debug_logging():
    """Display all logs from the Bot. May be useful while developing."""
    telebot.logger.setLevel(logging.DEBUG)
