from flask import Flask, request

import telebot
from telebot import types

import our_telebot
from our_telebot import GameBotHandler as OTB
import players
from players import Protagonist
import db.database
from db.database import DB
import world_map_class as wmc
import characters as npc
import quests as qw
import time





#*************************************************************************************
#*************************************************************************************
#*************************************************************************************
#*************************************************************************************

token = '6971180350:AAEEaXKPTSnEiYBzdIvLXo0rVQByQreZUbY'
secret = 'dfugvy78v7v8tw7v7cde9'
url = 'https://cursebow.pythonanywhere.com/' + secret

db = DB()
db.create_tables()
gamers_set = set()

bot = telebot.TeleBot(token, threaded=False)
bot.remove_webhook()
bot.set_webhook(url=url)


app = Flask(__name__)
@app.route('/'+secret, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200
#******************************************************************************************
#******************************************************************************************

def go_to_empty_bot(message, msg):
    """
    Sends a message to the specified chat ID using the `bot` object.

    Parameters:
        - message: The message object containing the chat ID.
        - msg: The message to send.

    Returns:
        None
    """
    bot.send_message(message.chat.id, msg, reply_markup = types.ReplyKeyboardRemove())

def go_to_authorizing_buttons(message):
    """
    Go to the authorizing buttons.

    Parameters:
        message (object): The message object.

    Returns:
        None
    """
    bot.clear_step_handler_by_chat_id(message.chat.id)
    markup = OTB.create_in_up_buttons()
    sender = bot.send_message(message.chat.id, "Здравствуй, путник", reply_markup=markup)
    bot.register_next_step_handler(sender, register_open)


@bot.message_handler(commands=['start'])
def handle_init(message):
    """
    Handles the 'start' command from the user and calls the 'go_to_authorizing_buttons'
    function with the provided message.

    Args:
        message (object): The message object containing information about the user's
            command.

    Returns:
        None
    """
    bot.clear_step_handler_by_chat_id(message.chat.id)
    go_to_authorizing_buttons(message)


# @bot.message_handler(commands=['players'])
# def show_players(message):
#     """
#     Retrieves a list of players from the database
#     and sends a message containing each player's name to the specified chat.

#     Parameters:
#     - message: The message object containing information about the chat.

#     Returns:
#     None
#     """
#     players = db.get_players()
#     for player in players:
#         bot.send_message(message.chat.id, player[1])


def register_open(message):
    """
    Registers the user in the system based on the message received.

    Parameters:
        message (obj): The message object received from the user.

    Returns:
        None
    """
    if message.text == 'Зарегистрироваться':
        go_to_register(message)
    elif message.text == 'Войти':
        go_to_sign_in(message)
    elif message.text == 'Отмена':
        go_to_empty_bot(message, 'Счастливого пути, странник')
    else:
        go_to_authorizing_buttons(message)


def go_to_register(message):
    """
    Send a message to the user with a cancel button and prompt them to enter their name.

    Parameters:
        message (obj): The message object received from the user.

    Returns:
        None
    """
    bot.clear_step_handler_by_chat_id(message.chat.id)
    markup = OTB.create_cancel_button()
    bot.send_message(message.chat.id, "Введи свое имя (никнейм)", reply_markup = markup)
    bot.register_next_step_handler(message, register)


def go_to_sign_in(message):
    """
    Sends a message to the user asking for their name and provides a cancel button.

    Parameters:
        message (object): The message object received from the user.

    Returns:
        None
    """
    bot.clear_step_handler_by_chat_id(message.chat.id)
    markup = OTB.create_cancel_button()
    bot.send_message(message.chat.id, "Как тебя зовут?", reply_markup = markup)
    bot.register_next_step_handler(message, login)


def go_to_register_continue(message, nickname):
    """
    Send a message to the user and register the next step handler.

    Args:
        message (Message): The message object containing information about the user's input.
        nickname (str): The nickname of the user.

    Returns:
        None
    """
    bot.clear_step_handler_by_chat_id(message.chat.id)
    sender = bot.send_message(message.chat.id, "Придумай пароль")
    bot.register_next_step_handler(sender, lambda m: register_continue(m, nickname))


def go_to_user_exists(message):
    """
    Sends a message to the user indicating that the given username
    is already taken and prompts them to choose another username.

    Parameters:
        message (unknown type): The message object containing information about the user and the chat.

    Returns:
        None
    """
    bot.clear_step_handler_by_chat_id(message.chat.id)
    bot.send_message(message.chat.id, "Имя уже занято. Придумай другое имя")
    bot.register_next_step_handler(message, register)


def register(message):
    """
    Register a user based on the provided message.

    Args:
        message (object): The message object containing the user input.

    Returns:
        None

    """
    if message.text == 'Отмена':
        go_to_authorizing_buttons(message)
        return
    if db.check_nickname_existence(message.text):
        go_to_register_continue(message, message.text)
    else:
        go_to_user_exists(message)


def register_continue(message, nickname):
    """
    Registers the continuation of the registration process.

    :param message: The message object containing information about the user's input.
    :type message: Message
    :param nickname: The nickname of the user.
    :type nickname: str
    """
    if message.text == 'Отмена':
        go_to_empty_bot(message, "Счастливого пути, странник")
        return
    go_to_register_confirm(message, nickname, message.text, "Подтверди пароль")


def go_to_register_confirm(message, nickname, password, msg):
    """
    Sends a message to the user and registers the next step handler.

    Args:
        message (unknown type): The message object containing information about the user and the chat.
        nickname (str): The nickname of the user.
        password (str): The password provided by the user.

    Returns:
        None
    """
    bot.clear_step_handler_by_chat_id(message.chat.id)
    sender = bot.send_message(message.chat.id, msg)
    bot.register_next_step_handler(sender, lambda m: register_confirm(m, nickname, password))


def go_to_npcs_menu(message, gamer):
    """
    Generates a menu for the non-playable characters (NPCs) in the game.

    Parameters:
        message (Message): The message object representing the user's input.
        gamer (Gamer): The gamer object representing the player.

    Returns:
        None
    """
    bot.clear_step_handler_by_chat_id(message.chat.id)
    npcs = gamer.get_current_location().get_npcs()
    markup = OTB.create_dict_buttons(npcs)
    sender = bot.send_message(message.chat.id, "Выбери персонажа", reply_markup = markup)
    bot.register_next_step_handler(sender, lambda m: handle_npcs(m, gamer))


def go_to_certain_npc_menu(message, gamer, npc_data):
    """
    Go to a certain NPC menu.

    Args:
        message (TelegramMessage): The message object.
        gamer (Player): The player object.
        npc (NPC): The NPC object.

    Returns:
        None
    """
    bot.clear_step_handler_by_chat_id(message.chat.id)
    markup = OTB.create_npcs_buttons()
    sender = bot.send_message(message.chat.id, 'Choose', reply_markup = markup)
    bot.register_next_step_handler(sender, lambda m: handle_npcs_action(m, gamer, npc_data))


def go_to_loactions_menu(message, gamer):
    """
    Generates a menu with the linked locations for the current gamer's location
    and sends it as a message to the specified chat. The function registers a
    callback to handle the user's choice of location.

    :param message: The message object that triggered this function
    :type message: Message
    :param gamer: The gamer object
    :type gamer: Gamer
    """
    print('invoked go_to_loactions_menu')
    bot.clear_step_handler_by_chat_id(message.chat.id)
    markup = OTB.create_location_buttons(gamer.get_current_location().get_linked_locations())
    sender = bot.send_message(message.chat.id, "Выбери локацию", reply_markup = markup)
    bot.register_next_step_handler(sender, lambda m: show_locations(m, gamer))


def go_to_enemies_menu(message, gamer):
    """
    Sends a message to the user to navigate to the enemies menu.

    :param message: The message object received from the user.
    :type message: any
    :param gamer: The gamer object representing the current user.
    :type gamer: Gamer
    """
    bot.clear_step_handler_by_chat_id(message.chat.id)
    markup = OTB.create_dict_buttons(gamer.get_current_location().get_enemies())
    sender = bot.send_message(message.chat.id, "ok, go to enemies list", reply_markup = markup)
    bot.register_next_step_handler(sender, lambda m : handle_enemies(m, gamer))


def go_to_top_game_menu(message, gamer, msg):
    """
    Generates a game menu and sends it to the specified chat ID.

    Parameters:
        message (telegram.Message): The message object that triggered the function.
        gamer (str): The username of the gamer.
        msg (str): The message to be displayed in the game menu.

    Returns:
        None
    """
    bot.clear_step_handler_by_chat_id(message.chat.id)
    markup = markup = OTB.create_game_buttons()
    sender = bot.send_message(message.chat.id, msg, reply_markup = markup)
    bot.register_next_step_handler(sender, lambda m : handle_game_top(m, gamer))


def register_confirm(message, nickname, password):
    """
    Registers confirmation for a user with a given message, nickname, and password.

    Parameters:
    - message (obj): The message object that triggered the registration confirmation.
    - nickname (str): The nickname of the user.
    - password (str): The password provided by the user.

    Returns:
    - None
    """
    if message.text == 'Отмена':
        go_to_empty_bot(message, "Счастливого пути, странник")
        return
    if message.text == password:
        create_and_initiate(message, nickname, password)
    else:
        go_to_register_confirm(message, nickname, password, "Пароли не совпадают. Попробуй ещё раз")


def create_and_initiate(message, nickname, password):
    """
    Creates a new user with the given nickname and password, and initiates a game for the user.

    Parameters:
        message (str): The message to be displayed during game initiation.
        nickname (str): The nickname of the user.
        password (str): The password of the user.

    Returns:
        None
    """
    db.create_user(nickname, password)
    gamer = Protagonist(nickname, wmc.Location('location_1'))
    gamers_set.add(gamer)
    initiate_game(message, gamer)


def login(message):
    """
    Log in the user based on the provided message.

    Parameters:
    - message (object): The message object containing the user input.

    Returns:
    - None

    Description:
    This function takes in a message object and extracts the user's nickname from it.
    If the nickname is 'Отмена', it calls the 'go_to_empty_bot' function and returns.
    If the nickname does not exist, it sends a message to the user saying that the user
    does not exist and registers the 'login' function as the next step handler.
    If the nickname exists, it sends a message to the user saying "Enter your password"
    and registers the 'login_load' function as the next step handler, passing the message
    and the nickname as parameters.
    """
    nickname = message.text
    if nickname == 'Отмена':
        go_to_empty_bot(message, "Счастливого пути, странник")
        return
    if  db.check_nickname_existence(nickname):
        bot.send_message(message.chat.id,
                        "Пользователь с таким именем не зарегистрирован")
        go_to_sign_in(message)
    else:
        go_to_login_load(message, nickname, "Введи пароль")


# **************************************************************GAME PROCESS LAUNCING
def login_load(message, nickname):
    """
    Login and load the user's data.

    Parameters:
        message (object): The message object containing the user's input.
        nickname (str): The nickname of the user.

    Returns:
        None
    """
    password = message.text
    if password == 'Отмена':
        go_to_empty_bot(message, "Счастливого пути, странник")
        return
    if not db.check_login_and_password(nickname, password):
        go_to_login_load(message, nickname, "Неверный пароль. Попробуй ещё раз")
    else:
        gamer = Protagonist(nickname, wmc.Location('location_1'))
        gamers_set.add(gamer)
        db.load_all_user_data(gamer)
        initiate_game(message, gamer)


def go_to_login_load(message, nickname, msg):
    """
    A function to go to the login load.

    Parameters:
    - message: The message object.
    - nickname: The nickname.
    - msg: The message.

    Returns:
    None
    """
    bot.clear_step_handler_by_chat_id(message.chat.id)
    sender = bot.send_message(message.chat.id, msg)
    bot.register_next_step_handler(sender, lambda m: login_load(m, nickname))


# **************************************************************GAME PROCESS LAUNCING
def initiate_game(message, gamer):
    """
    Initializes a new game with the given message and nickname.

    Args:
        message (str): The message object that triggered the game initiation.
        nickname (str): The nickname of the player initiating the game.

    Returns:
        None
    """
    bot.clear_step_handler_by_chat_id(message.chat.id)
    markup = OTB.create_game_buttons()
    sender = bot.send_message(message.chat.id, "Добро пожаловать в мир магии", reply_markup=markup)
    bot.register_next_step_handler(sender, lambda m : handle_game_top(m, gamer))


def handle_game_top(message, gamer):
    """
    Handle the top-level game menu based on the user's message.

    Args:
        message (obj): The message object containing the user's input.
        gamer (obj): The gamer object representing the current player.

    Returns:
        None.
    """
    if message.text == 'Персонажи':
        go_to_npcs_menu(message, gamer)
    elif message.text == 'Враги':
        go_to_enemies_menu(message, gamer)
    elif message.text == 'Карта':
        go_to_loactions_menu(message, gamer)
    elif message.text == 'Инвентарь':
        get_inventory(message, gamer)
    elif message.text == 'Герой':
        go_to_hero(message, gamer, 'Выбери действие')
    elif message.text == 'Выход':
        go_back_to_login(message, gamer)
        return
    else:
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, lambda m: handle_game_top(m, gamer))


def go_to_hero(message, gamer, msg):
    """
    Clears the step handler for the given chat ID. Creates a markup with hero buttons. Sends a message with the given text and the markup as a reply to the chat ID. Registers the next step handler with a lambda function that calls choose_hero_action with the next message and the gamer as parameters.

    Parameters:
        - message (obj): The message object.
        - gamer (obj): The gamer object.
        - msg (str): The text of the message to be sent.

    Returns:
        This function does not return anything.
    """
    bot.clear_step_handler_by_chat_id(message.chat.id)
    markup = OTB.create_hero_buttons()
    sender = bot.send_message(message.chat.id, msg, reply_markup = markup)
    bot.register_next_step_handler(sender, lambda m : choose_hero_action(m, gamer))


def choose_hero_action(message, gamer):
    """
    Choose the action for the hero based on the given message and gamer.

    Parameters:
        message (object): The message object containing the user input.
        gamer (object): The gamer object representing the player.

    Returns:
        None
    """
    if message.text == 'Назад':
        go_to_top_game_menu(message, gamer, 'Мир')
        return
    elif message.text == 'Квесты':
        get_quests(message, gamer)
    elif message.text == 'Инфо':
        get_info(message, gamer)
    elif message.text == 'Лечиться':
        if gamer.heal():
            go_to_hero(message, gamer, 'Лечение')
        else:
            go_to_hero(message, gamer, 'Нет подходящего зелья')
    elif message.text == 'Инвентарь':
        get_inventory(message, gamer)

def get_info(message, gamer):
    """
    Retrieves the information about the hero and sends it as a message to the specified chat.

    Parameters:
        message (telegram.Message): The message object that triggered the function.
        gamer (Gamer): The gamer object representing the player.

    Returns:
        None
    """
    hp, lvl = gamer.get_current_stats()
    sender = bot.send_message(message.chat.id, f"текущее здоровье: {hp}")
    sender = bot.send_message(message.chat.id, f"текущий уровень: {lvl}")
    bot.clear_step_handler_by_chat_id(message.chat.id)
    bot.register_next_step_handler(sender, lambda m: choose_hero_action(m, gamer))



def get_inventory(message, gamer):
    """
    Retrieves the inventory of a gamer and sends each item as a message to the specified chat.

    Parameters:
        message (telegram.Message): The message object that triggered the function.
        gamer (Gamer): The gamer object representing the player.

    Returns:
        None
    """
    inventory = gamer.get_inventory()
    for key, value in inventory.items():
        item_str = f"{key}: {value}"
        sender = bot.send_message(message.chat.id, item_str)
    bot.clear_step_handler_by_chat_id(message.chat.id)
    bot.register_next_step_handler(sender, lambda m: choose_hero_action(m, gamer))


def get_quests(message, gamer):
    markup = OTB.create_quests_list_buttons(gamer.get_current_quests())
    sender = bot.send_message(message.chat.id, "Квесты", reply_markup = markup)
    bot.clear_step_handler_by_chat_id(message.chat.id)
    bot.register_next_step_handler(sender, lambda m : choose_quest(m, gamer))


def choose_quest(message, gamer):
    """
    Retrieves the quests for a given gamer and sends them as a list of buttons in a Telegram message.

    Parameters:
    - message (telegram.Message): The message triggering the function.
    - gamer (Gamer): The gamer object to retrieve the quests for.

    Returns:
    None
    """
    if message.text == 'Назад':
        go_to_hero(message, gamer, 'Возвращаемся к герою')
        return
    else:
        for quest in gamer.get_current_quests():
            if message.text == quest.get_name():
                bot.send_message(message.chat.id, quest.get_task())
                bot.send_message(message.chat.id, quest.start_quest())
                if isinstance(quest, qw.SecretPotionQuest):
                    bot.send_message(message.chat.id, "Выполняем квест...")
                    time.sleep(1)
                    res = quest.perform()
                    if res:
                        result = f"Вы обнаружили {quest.artifact_name}!"
                    else:
                        result = f"К сожалению, {quest.artifact_name} не было найдено. Продолжайте поиски!"
                    sender = bot.send_message(message.chat.id, result)
                    gamer.remove_completed_quests()
                    get_quests(sender, gamer)
                else:
                    sender = bot.send_message(message.chat.id, "Напишите ответ:")
                    bot.clear_step_handler_by_chat_id(message.chat.id)
                    bot.register_next_step_handler(sender, lambda m: perfom_question_quest(m, gamer, quest))


def perfom_question_quest(message, gamer, quest):
    """
    Perform a question quest.

    Args:
        message (Type): The message object containing the text of the message.
        gamer (Type): The gamer object.
        quest (Type): The quest object.

    Returns:
        None
    """
    result = quest.perform(message.text)
    if result:
        bot.send_message(message.chat.id, "Верно! Загадка разгадана.")
        gamer.remove_completed_quests()
        get_quests(message, gamer)
    else:
        bot.send_message(message.chat.id, "Неверный ответ. Продолжайте разгадывать загадку.")
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.register_next_step_handler(message, lambda m: perfom_question_quest(m, gamer, quest))


def go_back_to_login(message, gamer):
    """
    Sends a "Bye" message to the user and removes the reply keyboard. Writes all user data to the database and registers the "register_open" function as the next step handler.

    Parameters:
        message (obj): The message object containing information about the user and the chat.
        gamer (str): The name of the gamer.

    Returns:
        None
    """
    bot.clear_step_handler_by_chat_id(message.chat.id)
    sender = bot.send_message(message.chat.id, "Bye", reply_markup = types.ReplyKeyboardRemove())
    db.write_all_user_data(gamer)
    bot.register_next_step_handler(sender, register_open)


def show_locations(message, gamer):
    """
    Show available locations based on user input.

    Args:
        message (obj): The message object containing the user input.
        gamer (obj): The gamer object representing the user.

    Returns:
        None
    """
    if message.text == 'Назад':
        go_to_top_game_menu(message, gamer, 'Мир')
        return
    else:
        locations_list = gamer.get_current_location().get_linked_locations()
        location = next((location for location in locations_list
                        if location['name'] == message.text), None)
        go_to_location_action(message, gamer, location)


def go_to_location_action(message, gamer, location):
    """
    Clears the step handler for the chat ID of the given message.
    Creates a location action buttons markup. Sends a message with the text "Ok"
    and the created markup to the chat ID of the given message.
    Registers the next step handler with the sender message to call the choose_action_of_location_menu function
    with the given message, gamer, and location as arguments.

    Args:
        message (Any): The message object.
        gamer (Any): The gamer object.
        location (Any): The location object.

    Returns:
        None
    """
    bot.clear_step_handler_by_chat_id(message.chat.id)
    markup = OTB.create_location_act_buttons()
    sender = bot.send_message(message.chat.id, "Ok", reply_markup = markup)
    bot.register_next_step_handler(sender, lambda m : choose_action_of_location_menu(m, gamer, location))


def choose_action_of_location_menu(message, gamer, choosen):
    """
    Generates the action to be taken based on the user's input in the location menu.

    Args:
        message (str): The user's input message.
        gamer (str): The gamer's information.
        choosen (str): The selected option from the menu.

    Returns:
        None
    """
    if message.text == 'Назад':
        go_to_loactions_menu(message, gamer)
    else:
        if message.text == 'Инфо':
            show_location_info(message, gamer, choosen)
        elif message.text == 'Перейти':
            go_to_location(message, gamer, choosen)


def show_location_info(message, gamer, choosen):
    """
    Generates a comment for the given function body in a markdown code block with the correct language syntax.

    Parameters:
        message (str): The message to be displayed.
        gamer (str): The gamer's name.
        choosen (str): The chosen description.

    Returns:
        None
    """
    bot.clear_step_handler_by_chat_id(message.chat.id)
    markup = OTB.create_location_act_buttons()
    sender = bot.send_message(message.chat.id, choosen['description'], reply_markup = markup)
    bot.register_next_step_handler(sender, lambda m : choose_action_of_location_menu(m, gamer, choosen))


def go_to_location(message, gamer, choosen):
    """
    Go to a specific location in the game.

    Parameters:
    - message: The message object that triggered the function.
    - gamer: The gamer object representing the player.
    - chosen: A dictionary containing the chosen location.

    Returns:
    None
    """
    name = gamer.get_current_location().get_linked_location_id_by_name(choosen['name'])
    gamer.go(wmc.Location(name))
    go_to_top_game_menu(message, gamer, 'Мир')


def handle_enemies(message, gamer):
    """
    Handles the selection of enemies in the game.

    Parameters:
    - message: The message object that triggered the function.
    - gamer: The gamer object representing the player.

    Returns:
    None
    """
    if message.text == 'Back':
        go_to_top_game_menu(message, gamer, 'Мир')
    else:
        enemies_data = gamer.get_current_location().get_full_enemies_data()
        enemy_name = message.text
        for enemy in enemies_data:
            if enemy['name'] == enemy_name:
                markup = OTB.create_enemy_buttons()
                bot.clear_step_handler_by_chat_id(message.chat.id)
                sender = bot.send_message(message.chat.id, 'Choose',
                                            reply_markup = markup)
                bot.register_next_step_handler(sender,
                                               lambda m: handle_enemies_action(m, gamer, enemy))
                break


def handle_enemies_action(message, gamer, enemy):
    """
    Handle the action performed by the enemies.

    Args:
        message (str): The message received.
        gamer (str): The gamer performing the action.
        enemy (str): The enemy being targeted.

    Returns:
        None
    """
    if message.text == 'Убежать':
        go_to_enemies_menu(message, gamer)
    elif message.text == 'Инфо':
        handle_enemy_info_showing(message, gamer, enemy)
    elif message.text == 'Бой':
        handle_enemy_fighting(message, gamer, enemy)


def get_description(message, desc_dict):
    """
    Generate a function comment for the given function body.

    Args:
        message (str): The message to process.
        desc_dict (dict): A dictionary containing descriptions.

    Returns:
        sender (str): The sender of the message.
    """
    for key in desc_dict.keys():
        if key != 'id' and key != 'dialog':
            sender = bot.send_message(message.chat.id, f"{key}: {desc_dict[key]}")
    return sender


def handle_enemy_info_showing(message, gamer, enemy):
    """
    Clears the step handler for the current chat ID and registers a new step handler for the given enemy.

    Parameters:
    - message: The message object representing the user's message.
    - gamer: The gamer object associated with the user.
    - enemy: The enemy object representing the enemy.

    Returns:
    None
    """
    bot.clear_step_handler_by_chat_id(message.chat.id)
    sender = get_description(message, enemy)
    bot.register_next_step_handler(sender,
                                   lambda m: handle_enemies_action(m, gamer, enemy))


def handle_enemy_fighting(message, gamer, enemy):
    """
    Handles enemy fighting.

    Args:
        message (object): The message object.
        gamer (object): The gamer object.
        enemy (object): The enemy object.

    Returns:
        None
    """
    art_count = gamer.check_current_arts_count()
    if gamer.attack(npc.Enemy(enemy)):
        bot.send_message(message.chat.id, 'Победа')
        if gamer.check_win_condition():
            if art_count != gamer.check_current_arts_count():
                bot.send_message(message.chat.id, 'Вы получили арт')
            go_to_top_game_menu(message, gamer, 'Вы прошли игру')
        else:
            go_to_enemies_menu(message, gamer)
    else:
        go_to_top_game_menu(message, gamer, 'Вы проиграли')


def handle_npcs(message, gamer):
    """
    Handles the interaction with non-player characters (NPCs) based on the user's message and the current state of the game.

    Parameters:
    - message (object): The message object containing the user's input.
    - gamer (object): The gamer object representing the current game state.

    Returns:
    None
    """
    if message.text == 'Назад':
        go_to_top_game_menu(message, gamer, 'Мир')
    else:
        npcs_data = gamer.get_current_location().get_full_npcs_data()
        for npc_data in npcs_data:
            if npc_data['name'] == message.text:
                go_to_certain_npc_menu(message, gamer, npc_data)
                break



def handle_npcs_action(message, gamer, npc_data):
    """
    Handles the action of NPCs based on the message received.

    Parameters:
    - message (str): The message received from the user.
    - gamer (str): The gamer object representing the user.
    - npc_data (str): The data of the NPC.

    Returns:
    - None
    """
    if message.text == 'Назад':
        go_to_npcs_menu(message, gamer)
    elif message.text == 'Инфо':
        sender = get_description(message, npc_data)
        bot.register_next_step_handler(sender, lambda m: handle_npcs_action(m, gamer, npc_data))
    elif message.text == 'Взять квест':
        assign_quest_to_hero(message, gamer, npc_data)
    elif message.text == 'Поговорить':
        talk_to_npc(message, gamer, npc_data)
    else:
        sender = bot.send_message(message.chat.id, "Такого действия нет")
        bot.register_next_step_handler(sender, lambda m: handle_npcs_action(m, gamer, npc_data))


def assign_quest_to_hero(message, gamer, npc_data):
    """
    Assigns a quest to a hero.

    Parameters:
    - message: The message object containing information about the chat.
    - gamer: The gamer object representing the hero.
    - npc_data: The data of the NPC offering the quest.

    Returns:
    None
    """
    npc_instance = npc.NPC(npc_data)
    quest_type, quest_id = npc_instance.offer_quest()
    quest = gamer.add_new_quest(quest_type, quest_id)
    bot.send_message(message.chat.id, f'Получен квест "{quest.get_name()}"')
    go_to_npcs_menu(message, gamer)




def talk_to_npc(message, gamer, npc_data):
    """
    Generates a comment for the given function body in a markdown code block with the correct language syntax.

    Args:
        message (str): The message to be processed.
        gamer (str): The gamer to interact with.
        npc_data (dict): The data of the NPC.

    Returns:
        None
    """
    npc_instance = npc.NPC(npc_data)
    msg = npc_instance.get_start_messages()
    ind_message = msg.ident

    next_msg_list = npc_instance.get_next_messages(ind_message)
    markup = OTB.create_answer_buttons(len(next_msg_list))
    bot.send_message(message.chat.id,
                              f"{npc_instance.name}: {msg.npc}", reply_markup=markup)
    for idx, msg in enumerate(next_msg_list, start=1):
        bot.send_message(message.chat.id, f"{idx}. {msg.user}")
    continue_conversation(message, gamer, npc_instance, ind_message)


def continue_conversation(message, gamer, npc_instance, ind_message):
    """
    Continue the conversation between the player and the non-player character (NPC).

    Args:
        message (TelegramMessage): The message object containing the user input.
        gamer (Gamer): The gamer object representing the player.
        npc_instance (NPC): The instance of the non-player character.
        ind_message (int): The index of the current message in the conversation.

    Returns:
        None

    Raises:
        None
    """
    if message.text == 'Окончить беседу':
        go_to_npcs_menu(message, gamer)
        return
    next_msg_list = npc_instance.get_next_messages(ind_message)
    if not next_msg_list or len(next_msg_list) == 0:
        bot.register_next_step_handler(message,
                               lambda m: continue_conversation(m, gamer, npc_instance, ind_message))

    if message.text != 'Поговорить':
        ind_message = next_msg_list[int(message.text) - 1].ident
        answer = npc_instance.get_messages(ind_message)
        if not answer:
            return
        bot.send_message(message.chat.id, f"{npc_instance.name}: {answer.npc}")
        next_msg_list = npc_instance.get_next_messages(ind_message)
        for idx, msg in enumerate(next_msg_list, start=1):
            bot.send_message(message.chat.id, f"{idx}. {msg.user}")
        markup = OTB.create_answer_buttons(len(next_msg_list))
        message = bot.send_message(message.chat.id, 'Выберите ответ', reply_markup=markup)
    bot.register_next_step_handler(message,
                                   lambda m: continue_conversation(m, gamer, npc_instance, ind_message))







