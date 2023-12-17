import logging
import time

import flask

# import telebot

import our_parser

API_TOKEN = "6739221276:AAE_0D3zfIZt9Y0xaP_lUjpZgobxzvi9OAs"

WEBHOOK_HOST = 'cursebow.pythonanywhere.com'
WEBHOOK_PORT = 8443
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_URL_BASE = f"https://{WEBHOOK_HOST}:{WEBHOOK_PORT}"
WEBHOOK_URL_PATH = f"/{API_TOKEN}/"

# WEBHOOK_SSL_CERT = './certs/webhook_cert.pem'
# WEBHOOK_SSL_PRIV = './certs/webhook_pkey.pem'




# bot = telebot.TeleBot(API_TOKEN, threaded=True)
# logger = telebot.logger
# telebot.logger.setLevel(logging.INFO)
# bot.remove_webhook()
# bot.polling()
# time.sleep(1)
# bot.set_webhook(url=f"{WEBHOOK_URL_BASE}{WEBHOOK_URL_PATH}",
#                 certificate = open(WEBHOOK_SSL_CERT, 'r'))

#debug----------------------------------------------------------------
# webhook_info = bot.get_webhook_info()
# if webhook_info.url:
#     print("Webhook is set")
#     print("Webhook URL:", webhook_info.url)
# else:
#     print("Webhook is not set")
#debug----------------------------------------------------------------


# @bot.message_handler(commands=['help', 'start'])
# def send_welcome(message):
#     bot.reply_to(message,
#                  ("Hi there, I am EchoBot.\n"
#                   "I am here to echo your kind words back to you."))


# @bot.message_handler(func=lambda message: True, content_types=['text'])
# def echo_message(message):
#     time.sleep(1)
#     bot.reply_to(message, message.text)


app = flask.Flask(__name__)


@app.route('/', methods=['GET', 'HEAD'])
def index():
    json_string = flask.request.get_data().decode('utf-8')
    print(json_string)
    return ' Hello, World!'

# @app.route(WEBHOOK_URL_PATH, methods=['POST'])
# def webhook():
#     print("abc")
#     if flask.request.headers.get('content-type') == 'application/json':
#         json_string = flask.request.get_data().decode('utf-8')
#         update = telebot.types.Update.de_json(json_string)
#         bot.process_new_updates([update])
#         return ''
#     else:
#         flask.abort(403)


# app.run(host=WEBHOOK_LISTEN,
#         port=WEBHOOK_PORT,
#         ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
#         debug=True
#         )

