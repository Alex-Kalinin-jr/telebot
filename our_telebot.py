import telebot
from telebot import TeleBot, types


class GameBotHandler():

    @staticmethod
    def create_cancel_button():
        markup = types.ReplyKeyboardMarkup()
        markup.add('Отмена')
        return markup

    @staticmethod
    def create_in_up_buttons():
        markup = types.ReplyKeyboardMarkup()
        markup.add(types.KeyboardButton(text = "Зарегистрироваться"),
                   types.KeyboardButton(text = "Войти"),
                   types.KeyboardButton(text = "Отмена"))
        return markup

    @staticmethod
    def create_game_buttons():
        markup = types.ReplyKeyboardMarkup()
        markup.row(types.KeyboardButton(text = "Персонажи"),
                   types.KeyboardButton(text = "Враги"))
        markup.row(types.KeyboardButton(text = "Инвентарь"),
                   types.KeyboardButton(text = "Карта"),)
        markup.row(types.KeyboardButton(text = "Герой"),
                   types.KeyboardButton(text = "Выход"))
        return markup


    @staticmethod
    def create_dict_buttons(npc_dict):
        markup = types.ReplyKeyboardMarkup()
        for word in npc_dict:
            value = list(word.values())[0]
            markup.add(types.KeyboardButton(text = value))
        markup.row(types.KeyboardButton(text = "Назад"))
        return markup


    @staticmethod
    def create_location_buttons(locations):
        markup = types.ReplyKeyboardMarkup()
        for location in locations:
            value = location['name']
            markup.add(types.KeyboardButton(text = value))
        markup.row(types.KeyboardButton(text = "Назад"))
        return markup

    @staticmethod
    def create_enemy_buttons():
        markup = types.ReplyKeyboardMarkup()
        markup.row(types.KeyboardButton(text = "Инфо"),
                   types.KeyboardButton(text = "Бой"),
                   types.KeyboardButton(text = "Back"))
        return markup


    @staticmethod
    def create_npcs_buttons():
        markup = types.ReplyKeyboardMarkup()
        markup.row(types.KeyboardButton(text = "Инфо"),
                   types.KeyboardButton(text = "Взять квест"),
                   types.KeyboardButton(text = "Поговорить"),
                   types.KeyboardButton(text = "Назад"))
        return markup


    @staticmethod
    def create_location_act_buttons():
        markup = types.ReplyKeyboardMarkup()
        markup.row(types.KeyboardButton(text = "Инфо"),
                   types.KeyboardButton(text = "Перейти"),
                   types.KeyboardButton(text = "Назад"))
        return markup

    @staticmethod
    def create_locations_buttons(locations):
        markup = types.ReplyKeyboardMarkup()
        for word in locations:
            markup.add(types.KeyboardButton(text = word['name']))
        markup.row(types.KeyboardButton(text = "Back"))
        return markup

    @staticmethod
    def create_hero_buttons():
        markup = types.ReplyKeyboardMarkup()
        markup.row(
                   types.KeyboardButton(text = "Инвентарь"),
                   types.KeyboardButton(text = "Инфо"),
                   types.KeyboardButton(text = "Лечиться"))
        markup.row(
                   types.KeyboardButton(text = "Квесты"),
                   types.KeyboardButton(text = "Назад"))
        return markup

    @staticmethod
    def create_quests_list_buttons(quests):
        markup = types.ReplyKeyboardMarkup()
        for quest in quests:
            markup.add(types.KeyboardButton(text = quest.get_name()))
        markup.row(types.KeyboardButton(text = "Назад"))
        return markup

    @staticmethod
    def create_quests_list_buttons(quests):
        markup = types.ReplyKeyboardMarkup()
        for quest in quests:
            markup.add(types.KeyboardButton(text = quest.get_name()))
        markup.row(types.KeyboardButton(text = "Назад"))
        return markup

    @staticmethod
    def create_answer_buttons(count):
        markup = types.ReplyKeyboardMarkup()
        for i in range(count):
            markup.add(types.KeyboardButton(text = i+1))
        markup.row(types.KeyboardButton(text = "Окончить беседу"))
        return markup


