import telebot
from telebot import TeleBot, types


menus = {"User" : ["Sign up", "Sign in"],
        "Init": ["World", "Stats"],
        "World": ["Move", "Characters"],
        }

class GameBotHandler():

    @staticmethod
    def create_in_up_buttons(bot, message):
        markup = types.ReplyKeyboardMarkup()
        markup.add(types.KeyboardButton(text = "Sign up"),
                   types.KeyboardButton(text = "Sign in"))
        bot.send_message(message.chat.id, "Welcome", reply_markup=markup)

    @staticmethod
    def create_user_in_db(bot, message):
        markup = types.ReplyKeyboardMarkup()
        markup.add(types.KeyboardButton(text = "Sign up"),
                   types.KeyboardButton(text = "Sign in"))
        bot.send_message(message.chat.id, "Welcome", reply_markup=markup)









    # def CreateNpcButtons(self, message):
    #     markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    #     chars = types.KeyboardButton("cButton 1")
    #     items = types.KeyboardButton("cButton 2")
    #     back_bttn = types.KeyboardButton("cBack")
    #     markup.add(chars, items, back_bttn)
    #     self.send_message(message.chat.id, "this is the wrapper to characters",
    #                     reply_markup=markup)


    # def CreateItemsButtons(self, message):
    #     markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    #     chars = types.KeyboardButton("iButton 1")
    #     items = types.KeyboardButton("iButton 2")
    #     back_bttn = types.KeyboardButton("iBack")
    #     markup.add(chars, items, back_bttn)
    #     self.send_message(message.chat.id, "this is the wrapper to items",
    #                       reply_markup=markup)
#********************************************************************************


        # start callbacks
        # @.message_handler(commands=['start'])
        # def handle_init(self, message):
        #     self.CreateInitButtons(message)

        # # first level callbacks
        # @self.bot.message_handler(func=lambda message: message.text == "Map")
        # def characters_reply(self, message):
        #     self.CreateNpcButtons(message)

        # @self.bot.message_handler(func=lambda message: message.text == "Items")
        # def items_reply(self, message):
        #     self.CreateItemsButtons(message)

        # # second level callbacks
        # @self.bot.message_handler(func=lambda message: message.text == "Move 1")
        # def handle_cButton1(self, message):
        #     self.send_message(message.chat.id, "cButton 1 pressed")


        # @self.bot.message_handler(func=lambda message: message.text == "Move 2")
        # def handle_cButton2(self, message):
        #     self.send_message(message.chat.id, "cButton 2 pressed")

        # @self.bot.message_handler(func=lambda message: message.text == "cBack")
        # def handle_cBack(self, message):
        #     self.CreateInitButtons(message)

        # @self.bot.message_handler(func=lambda message: message.text == "iButton 1")
        # def handle_iButton1(self, message):
        #     self.send_message(message.chat.id, "iButton 1 pressed")

        # @self.bot.message_handler(func=lambda message: message.text == "iButton 2")
        # def handle_iButton2(self, message):
        #     self.send_message(message.chat.id, "iButton 2 pressed")

        # @self.bot.message_handler(func=lambda message: message.text == "iBack")
        # def handle_iBack(self, message):
        #     self.CreateInitButtons(message)

#functions
#********************************************************************************