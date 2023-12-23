import sys
import os
import json
import logging
import sqlite3

import telebot
from telebot import types

from our_telebot import GameBotHandler as OTB

#***************************************************************
conn = sqlite3.connect('db/users.db')
cur = conn.cursor()
# cur.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT, password TEXT)')
# conn.commit()
#***************************************************************
locations: dict
current_location: dict
try:
    f = open('db/locations.json', 'r')
    locations = json.load(f)
    cur.execute('CREATE TABLE IF NOT EXISTS locations(name TEXT, description TEXT, linked_locations TEXT)')
    for location in locations.keys():
        for linked in locations[location]["linked_locations"]:
            cur.execute('INSERT INTO locations(name, description, linked_locations) VALUES(?, ?, ?)',
                    (location, locations[location]["description"], linked))
    conn.commit()
    current_location = locations["Forest of Whispers"]
    f.close()
except FileNotFoundError:
    print("File not found: .db/locations.json")


#***************************************************************
token = '6971180350:AAFb9GyaljG2ah6YPjteAHXXckjMNOe7oSQ'
bot = telebot.TeleBot(token, threaded=False)
#***************************************************************


@bot.message_handler(commands=['start'])
def handle_init(message):
    OTB.create_in_up_buttons(bot, message)
    bot.register_next_step_handler(message, register_open)


@bot.message_handler(commands=['players'])
def show_players(message):
    players = cur.execute("SELECT * FROM users").fetchall()
    for player in players:
        bot.send_message(message.chat.id, player[1])

@bot.message_handler(commands=['players'])
def show_players(message):
    players = cur.execute("SELECT * FROM users").fetchall()
    for player in players:
        bot.send_message(message.chat.id, player[1])


def register_open(message):
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Enter your nickname", reply_markup = markup)
    if message.text == 'Sign up':
        bot.register_next_step_handler(message, register)
    elif message.text == 'Sign in':
        bot.register_next_step_handler(message, login)


def register(message):
    nickname = message.text
    existence_checker = cur.execute("SELECT * FROM users WHERE name = ?", (nickname,)).fetchall()
    if existence_checker == []:
        passer = bot.send_message(message.chat.id, "Now enter your password")
        bot.register_next_step_handler(passer, lambda m: register_continue(m, nickname))
    else:
        bot.send_message(message.chat.id, "User already exists. Enter another name")
        bot.register_next_step_handler(message, register)


def register_continue(message, nickname):
    password = message.text
    passer = bot.send_message(message.chat.id, "Confirm your password")
    bot.register_next_step_handler(passer, lambda m: register_confirm(m, nickname, password))


def register_confirm(message, nickname, password):
    if message.text == password:
        cur.execute("INSERT INTO users(name, password) VALUES(?, ?)", (nickname, password))
        conn.commit()
        bot.send_message(message.chat.id, "Success")
    else:
        passer = bot.send_message(message.chat.id, "Passwords do not match. Try again")
        bot.register_next_step_handler(passer, lambda m: register_confirm(m, nickname, password))


def login(message):
    nickname = message.text
    existence_checker = cur.execute("SELECT * FROM users WHERE name = ?", (nickname,)).fetchall()
    if existence_checker == []:
        bot.send_message(message.chat.id, "User does not exist. Try again")
        bot.register_next_step_handler(message, login)
    else:
        passer = bot.send_message(message.chat.id, "Enter your password")
        bot.register_next_step_handler(passer, lambda m: login_load(m, nickname))


def login_load(message, nickname):
    password = message.text
    existence_checker = cur.execute("SELECT * FROM users WHERE name = ? AND password = ?",
                                    (nickname, password)).fetchall()
    if existence_checker == []:
        passer = bot.send_message(message.chat.id, "Wrong password. Try again")
        bot.register_next_step_handler(passer, lambda m: login_load(m, nickname))
    else:
        bot.send_message(message.chat.id, "Success")
        print(existence_checker)




bot.infinity_polling()










# @bot.callback_query_handler(func=lambda call: call.data == 'Init')
# def world_reply(call):
#     if call.message.text == 'World':
#         OTB.CreateButtons(bot, call.message, 'World', menus["World"])
#     elif call.message.text == 'Stats':
#         #to be handled
#         pass


# @bot.message_handler(func=lambda message: message.data == "World")
# def location_reply(message):
#     if message.text == 'Map':
#         if current_location is not None:
#             OTB.CreateButtons(bot, message, 'Move',
#                               current_location["linked_locations"])
#         else:
#             current_location = locations["Forest of Whispers"]
#             OTB.CreateButtons(bot, message, 'Move',
#                               current_location["linked_locations"])
#     elif message.text == 'Actions':
#         #to be handled
#         bot.send_message(message.chat.id, "Welcome to actions")


# @bot.message_handler(func=lambda message: message.data == "Map")
# def move_reply(message):
#         current_location = message.text
#         OTB.CreateButtons(bot, message, 'World', menus["World"])






#*************************************************************************************
#*************************************************************************************
#*************************************************************************************
#*************************************************************************************

# import telebot
# from telebot import types
# from flask import Flask, request

# token = '6769840382:AAFAdvy-2e2VozIQGTIMYYluRaPPR9Ea6rA'
# secret = 'dfugvy78v7v8tw7v7cde9'
# url = 'https://cursebow.pythonanywhere.com/' + secret

# bot = telebot.TeleBot(token, threaded=False)
# bot.remove_webhook()
# bot.set_webhook(url=url)

# menus_list = { "Init": ["World", "Stats"],
#                 "World": ["Move", "Characters"],
#                 }


# app = Flask(__name__)
# @app.route('/'+secret, methods=['POST'])
# def webhook():
#     update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
#     bot.process_new_updates([update])
#     return 'ok', 200



# @bot.message_handler(commands=['start'])
# def handle_init(message):
#     CreateInitButtons(message, menus_list['Init'])

# def CreateInitButtons(message, menus):
#     markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
#     for menu in menus:
#         bttn = types.KeyboardButton(menu)
#         markup.add(bttn)
#     bot.send_message(message.chat.id, "Welcome",
#                       reply_markup=markup)