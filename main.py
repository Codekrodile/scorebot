import telebot
# import mongodatabase
# import functions

# import config
# API_KEY = config.API_KEY
# valid_id = [int(id) for id in config.VALID_ID.split(';')]

import os
from flask import Flask, request
API_KEY = os.environ.get("API_KEY", None)
valid_id = [int(id) for id in os.environ.get("VALID_ID", None).split(';')]

scoreboard = {"A":0, "B":0, "C":0, "CSS":0, "SHQ":0}
bot = telebot.TeleBot(API_KEY)
server = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(msg):
    #validate id
    if msg.chat.id in valid_id:
        text = "Welcome to scorebot! \n\ninstructions to update the scoreboard \n/update <A/B/C/CSS/SHQ> <points earned> \neg. \n/update A 3 \n/update CSS -5 \n\n/explore to see what a telebot can do"

        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton("display", callback_data="display"))

        bot.send_message(msg.chat.id, text, reply_markup=keyboard)
    
    else:
        bot.send_message(msg.chat.id, "u do not have access to the bot, pls walk away...")
        alert = f"id entry at start command \nuser id: {msg.from_user.id} \nis_bot: {msg.from_user.is_bot} \nfirst name: {msg.from_user.first_name} \nusername: {msg.from_user.username} \nlast name: {msg.from_user.last_name}"
        bot.send_message(valid_id[0], alert)

@bot.message_handler(commands=['update'])
def update(msg):
    #validate id
    if msg.chat.id in valid_id:
        text = "invalid input"
        if len(msg.text.split(' ')) == 3:
            try:
                flt, points = msg.text.split(' ')[1], int(msg.text.split(' ')[2])

                if flt in ['A', 'B', 'C', 'CSS', 'SHQ']:
                    scoreboard[flt] = scoreboard[flt] + points
                    text = f"{flt} has earned {points} points"
            except:
                pass

        bot.send_message(msg.chat.id, text)
    
    else:
        bot.send_message(msg.chat.id, "u do not have access to the bot, pls walk away...")
        alert = f"id entry at start command \nuser id: {msg.from_user.id} \nis_bot: {msg.from_user.is_bot} \nfirst name: {msg.from_user.first_name} \nusername: {msg.from_user.username} \nlast name: {msg.from_user.last_name}"
        bot.send_message(valid_id[0], alert)

@bot.callback_query_handler(func=lambda call: call.data == "display")
def display(call):
    bot.answer_callback_query(call.id) #required to remove the loading state, which appears upon clicking the button

    #validate id
    if call.message.chat.id in valid_id:
        text = f'''DISPLAY

┌───── •✧✧• ─────┐
        SCOREBOARD
        A   : {scoreboard["A"]}
        B   : {scoreboard["B"]}
        C   : {scoreboard["C"]}
        CSS : {scoreboard["CSS"]}
        SHQ : {scoreboard["SHQ"]}
└───── •✧✧• ─────┘
'''

        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton("refresh", callback_data="display"), 
        )
        
        bot.edit_message_text(
            text= text,
            chat_id= call.message.chat.id,
            message_id= call.message.message_id,
            reply_markup= keyboard
        )
    
    else:
        bot.send_message(call.message.chat.id, "u do not have access to the bot, pls walk away...")


###########################################################################################################3
@bot.message_handler(commands=['explore'])
def explore(msg):
    #validate id
    if msg.chat.id in valid_id:
        text = "this is the explore section to understand what can a telebot do! click the button below to get started:)"

        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton("menu", callback_data="menu"))

        bot.send_message(msg.chat.id, text, reply_markup=keyboard)
    
    else:
        bot.send_message(msg.chat.id, "u do not have access to the bot, pls walk away...")
        alert = f"id entry at start command \nuser id: {msg.from_user.id} \nis_bot: {msg.from_user.is_bot} \nfirst name: {msg.from_user.first_name} \nusername: {msg.from_user.username} \nlast name: {msg.from_user.last_name}"
        bot.send_message(valid_id[0], alert)

@bot.message_handler(commands=['hello'])
def hello(msg):
    #validate id
    if msg.chat.id in valid_id:
        text = f"hello {msg.from_user.first_name} {msg.from_user.last_name} \n\nye i can get ur name too HAHAHA"
        bot.send_message(msg.chat.id, text)
    
    else:
        bot.send_message(msg.chat.id, "u do not have access to the bot, pls walk away...")
        alert = f"id entry at start command \nuser id: {msg.from_user.id} \nis_bot: {msg.from_user.is_bot} \nfirst name: {msg.from_user.first_name} \nusername: {msg.from_user.username} \nlast name: {msg.from_user.last_name}"
        bot.send_message(valid_id[0], alert)

@bot.callback_query_handler(func=lambda call: call.data == "menu")
def handle_menu(call):
    bot.answer_callback_query(call.id) #required to remove the loading state, which appears upon clicking the button

    #validate id
    if call.message.chat.id in valid_id:
        text = "scoreboard \n\nthese are some buttons, there can be a max of 4 buttons in a row, press button 1 or 2 to explore the options \n\nalso try /hello"

        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton("button1", callback_data="button1")
        )
        keyboard.row(
            telebot.types.InlineKeyboardButton("button2", callback_data="button2"), 
            telebot.types.InlineKeyboardButton("button3", callback_data="nowhere")
        )
        keyboard.row(
            telebot.types.InlineKeyboardButton("button4", callback_data="button1"), 
            telebot.types.InlineKeyboardButton("button5", callback_data="nowhere"),
            telebot.types.InlineKeyboardButton("button6", callback_data="nowhere")
        )
        keyboard.row(
            telebot.types.InlineKeyboardButton("button7", callback_data="nowhere"), 
            telebot.types.InlineKeyboardButton("button8", callback_data="nowhere"),
            telebot.types.InlineKeyboardButton("button9", callback_data="nowhere"),
            telebot.types.InlineKeyboardButton("button10", callback_data="nowhere")
        )
        keyboard.row(
            telebot.types.InlineKeyboardButton("Contact dev codekrodile", url="telegram.me/loueyy")
        )
        
        bot.edit_message_text(
            text= text,
            chat_id= call.message.chat.id,
            message_id= call.message.message_id,
            reply_markup= keyboard
        )
    
    else:
        bot.send_message(call.message.chat.id, "u do not have access to the bot, pls walk away...")

@bot.callback_query_handler(func=lambda call: call.data == "button1")
def handle_button1(call):
    bot.answer_callback_query(call.id) #required to remove the loading state, which appears upon clicking the button

    #validate id
    if call.message.chat.id in valid_id:

        text = 'welcome to button 1! \ni can display some stuff in the message, or in the buttons. currently all the buttons have no functions, but i can customise them, like the back button'
        keyboard = telebot.types.InlineKeyboardMarkup()

        keyboard.row(
            telebot.types.InlineKeyboardButton("sample", callback_data="nowhere"),
            telebot.types.InlineKeyboardButton("display", callback_data="nowhere"),
            telebot.types.InlineKeyboardButton("here", callback_data="nowhere")
        )
        keyboard.row(
            telebot.types.InlineKeyboardButton("buttons", callback_data="nowhere"), 
            telebot.types.InlineKeyboardButton("have", callback_data="nowhere"), 
            telebot.types.InlineKeyboardButton("no", callback_data="nowhere"),
            telebot.types.InlineKeyboardButton("functions", callback_data="nowhere")
        )
        keyboard.add(telebot.types.InlineKeyboardButton(text="back", callback_data="scoreboard"))
        
        bot.edit_message_text(
            text= text,
            chat_id= call.message.chat.id,
            message_id= call.message.message_id,
            reply_markup= keyboard
        )

    else:
        bot.send_message(call.message.chat.id, "u do not have access to the bot, pls walk away...")

@bot.callback_query_handler(func=lambda call: call.data == "button2")
def handle_button2(call):
    bot.answer_callback_query(call.id) #required to remove the loading state, which appears upon clicking the button

    #validate id
    if call.message.chat.id in valid_id:

        text = '''welcome to button 2! 

i can use this message as display as well!

╭━┳━╭━╭━╮╮
┃┈┈┈┣▅╋▅┫┃
┃┈┃┈╰━╰━━━━━━╮
╰┳╯┈┈┈┈┈┈┈┈┈◢▉◣
╲┃┈┈┈┈┈┈┈┈┈▉▉▉
╲┃┈┈┈┈┈┈┈┈┈◥▉◤
╲┃┈┈┈┈╭━┳━━━━╯
╲┣━━━━━━┫
'''
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton(text="back", callback_data="scoreboard"))
        
        bot.edit_message_text(
            text= text,
            chat_id= call.message.chat.id,
            message_id= call.message.message_id,
            reply_markup= keyboard
        )

    else:
        bot.send_message(call.message.chat.id, "u do not have access to the bot, pls walk away...")

# bot.polling()

@server.route('/' + API_KEY, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://lckhappysquadbot.herokuapp.com/" + API_KEY)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
