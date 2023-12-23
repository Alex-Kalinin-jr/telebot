from random import random

import telebot
from telebot import TeleBot, types


class GameBotHandler():

    @staticmethod
    def create_cancel_button():
        """
        Create a cancel button for a ReplyKeyboardMarkup.

        Returns:
            types.ReplyKeyboardMarkup: The created cancel button markup.
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('❌ Отмена')
        return markup

    @staticmethod
    def create_in_up_buttons():
        """
        Creates a ReplyKeyboardMarkup with three buttons: "🛃 Зарегистрироваться", "✅ Войти", and "❌ Отмена".

        Returns:
            types.ReplyKeyboardMarkup: The created ReplyKeyboardMarkup object.
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton(text = "🛃 Зарегистрироваться"),
                   types.KeyboardButton(text = "✅ Войти"),
                   types.KeyboardButton(text = "❌ Отмена"))
        return markup


    @staticmethod
    def create_game_buttons():
        """
        Creates game buttons for the user interface.

        Returns:
            types.ReplyKeyboardMarkup: The markup containing the game buttons.
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(types.KeyboardButton(text = "👩‍🎨 Персонажи"),
                   types.KeyboardButton(text = "🧛‍♂️ Враги"))
        markup.row(types.KeyboardButton(text = "🧳 Инвентарь"),
                   types.KeyboardButton(text = "🌍 Карта"),)
        markup.row(types.KeyboardButton(text = "🥷 Герой"),
                   types.KeyboardButton(text = "❌ Выход"))
        return markup

    @staticmethod
    def create_dict_buttons(npc_dict):
        """
        Generate a ReplyKeyboardMarkup with buttons based on the given npc_dict.

        Args:
            npc_dict (dict): A dictionary containing the NPC data.

        Returns:
            types.ReplyKeyboardMarkup: The generated ReplyKeyboardMarkup object.
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for word in npc_dict:
            value = list(word.values())[0]
            markup.add(types.KeyboardButton(text = f'👳 {value}'))
        markup.row(types.KeyboardButton(text = "❌ Назад"))
        return markup


    @staticmethod
    def create_location_buttons(locations):
        """
        Create location buttons for a given list of locations.

        Args:
            locations (list): A list of locations.

        Returns:
            types.ReplyKeyboardMarkup: The markup containing the location buttons.
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for location in locations:
            value = '🌏 ' + location['name']
            markup.add(types.KeyboardButton(text = value))
        markup.row(types.KeyboardButton(text = "❌ Назад"))
        return markup

    @staticmethod
    def create_enemy_buttons():
        """
        Creates enemy buttons for the user interface.

        Returns:
            types.ReplyKeyboardMarkup: The created markup for the enemy buttons.
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(types.KeyboardButton(text = "❓ Инфо"),
                   types.KeyboardButton(text = "⚔️ Бой"),
                   types.KeyboardButton(text = "❌ Назад"))
        return markup


    @staticmethod
    def create_npcs_buttons():
        """
        Creates a ReplyKeyboardMarkup object with buttons for interacting with NPCs.

        Returns:
            types.ReplyKeyboardMarkup: The ReplyKeyboardMarkup object with the NPC buttons.
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(types.KeyboardButton(text = "❓ Инфо"),
                   types.KeyboardButton(text = "🧩 Взять квест"),
                   types.KeyboardButton(text = "🗣 Поговорить"),
                   types.KeyboardButton(text = "❌ Назад"))
        return markup


    @staticmethod
    def create_location_act_buttons():
        """
        Creates a set of location action buttons for a chatbot.

        Returns:
            types.ReplyKeyboardMarkup: The created ReplyKeyboardMarkup object.
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(types.KeyboardButton(text = "❓ Инфо"),
                   types.KeyboardButton(text = "⏩ Перейти"),
                   types.KeyboardButton(text = "❌ Назад"))
        return markup

    @staticmethod
    def create_locations_buttons(locations):
        """
        Creates a ReplyKeyboardMarkup with buttons for each location.

        Args:
            locations (list): A list of dictionaries representing locations. Each dictionary should have a 'name' key.

        Returns:
            types.ReplyKeyboardMarkup: The created ReplyKeyboardMarkup object.
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for word in locations:
            markup.add(types.KeyboardButton(text = word['name']))
        markup.row(types.KeyboardButton(text = "Back"))
        return markup

    @staticmethod
    def create_hero_buttons():
        """
        Create and return a ReplyKeyboardMarkup object containing hero buttons.

        This static method creates a ReplyKeyboardMarkup object with hero buttons
        for the user interface. The buttons include "🧳 Инвентарь", "Инфо",
        "Лечение", "Квесты", and "Назад". The resize_keyboard parameter
        is set to True to allow the keyboard to be resized.

        Returns:
            markup (types.ReplyKeyboardMarkup): The created ReplyKeyboardMarkup object.
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(
                   types.KeyboardButton(text = "🧳 Инвентарь"),
                   types.KeyboardButton(text = "❓ Инфо"),
                   types.KeyboardButton(text = "➕ Лечение"))
        markup.row(
                   types.KeyboardButton(text = "🧩 Квесты"),
                   types.KeyboardButton(text = "❌ Назад"))
        return markup

    @staticmethod
    def create_quests_list_buttons(quests):
        """
        Create a list of buttons for the given quests.

        Args:
            quests (list): A list of quest objects.

        Returns:
            markup (types.ReplyKeyboardMarkup): The keyboard markup with the buttons.
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for quest in quests:
            markup.add(types.KeyboardButton(text = quest.get_name()))
        markup.row(types.KeyboardButton(text = "❌ Назад"))
        return markup


    @staticmethod
    def create_answer_buttons(count):
        """
        Creates a reply keyboard markup with the specified number of answer buttons.

        :param count: An integer representing the number of answer buttons to create.
        :return: A ReplyKeyboardMarkup object containing the reply keyboard markup.
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in range(count):
            markup.add(types.KeyboardButton(text = i+1))
        markup.row(types.KeyboardButton(text = "❌ Окончить беседу"))
        return markup
