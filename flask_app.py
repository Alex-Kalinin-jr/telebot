import telebot
from flask import Flask, request

token = '6769840382:AAFAdvy-2e2VozIQGTIMYYluRaPPR9Ea6rA'
secret = 'dfugvy78v7v8tw7v7cde9'
url = 'https://cursebow.pythonanywhere.com/' + secret

bot = telebot.TeleBot(token, threaded=False)
bot.remove_webhook()
bot.set_webhook(url=url)

app = Flask(__name__)
@app.route('/'+secret, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200


@bot.message_handler(commands=['start'])
def handle_init(self, message):
    CreateInitButtons(message)

def CreateInitButtons(self,message, menus):
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    for menu in menus:
        bttn = types.KeyboardButton(menu)
        markup.add(bttn)
    self.send_message(message.chat.id, "Welcome",
                      reply_markup=markup)