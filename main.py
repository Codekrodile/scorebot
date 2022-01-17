import telebot
import mongodatabase
import functions

import config
API_KEY = config.API_KEY
valid_id = [int(id) for id in config.VALID_ID.split(';')]
link = config.LINK
db_name = config.DB_NAME

# import os
# from flask import Flask, request
# API_KEY = os.environ.get("API_KEY", None)
# valid_id = [int(id) for id in os.environ.get("VALID_ID", None).split(';')]
# link = os.environ.get("LINK", None)
# db_name = os.environ.get("DB_NAME", None)
# server = Flask(__name__)

db = mongodatabase.Database(link, db_name)
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])
def start(msg):
    if msg.chat.id in valid_id: #validate id
        text = '''Welcome to scorebot!
        
Commands
/display
    view scoreboard

/update <game> <team(s)> <points>
    update the team's or teams' point for the specified game
    team: a, b, c, css or shq
    games: bball, soccer, carrom, dart or foosball

    eg.
    /update bball A 3
    /update carrom CSS -5
    /update soccer B C SHQ 1
'''

        bot.send_message(msg.chat.id, text)
    
    else:
        bot.send_message(msg.chat.id, "u do not have access to the bot, pls walk away...")
        alert = f"id entry at start command \nuser id: {msg.from_user.id} \nis_bot: {msg.from_user.is_bot} \nfirst name: {msg.from_user.first_name} \nusername: {msg.from_user.username} \nlast name: {msg.from_user.last_name}"
        bot.send_message(valid_id[0], alert)

@bot.message_handler(commands=['update'])
def update(msg):
    if msg.chat.id in valid_id: #validate id
        game, teams, point = functions.format_input(msg.text)
        if game == -1: #invalid input
            text = point
        
        else:
            #update db
            for team in teams:
                db.update_scoreboard(game, team, point)

            text = f"{game}: {teams} won {point} points"

        bot.send_message(msg.chat.id, text)
    
    else:
        bot.send_message(msg.chat.id, "u do not have access to the bot, pls walk away...")
        alert = f"id entry at update command \nuser id: {msg.from_user.id} \nis_bot: {msg.from_user.is_bot} \nfirst name: {msg.from_user.first_name} \nusername: {msg.from_user.username} \nlast name: {msg.from_user.last_name}"
        bot.send_message(valid_id[0], alert)

@bot.message_handler(commands=['display'])
def display(msg):
    if msg.chat.id in valid_id: #validate id
        #display total scoreboard
        text = functions.display_total_scoreboard(db.get_total_scoreboard())

        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton("Sport", callback_data="sport"), 
            telebot.types.InlineKeyboardButton("Mess", callback_data="mess")
        )
        bot.send_message(msg.chat.id, text, reply_markup=keyboard)

    else:
        bot.send_message(msg.chat.id, "u do not have access to the bot, pls walk away...")
        alert = f"id entry at display command \nuser id: {msg.from_user.id} \nis_bot: {msg.from_user.is_bot} \nfirst name: {msg.from_user.first_name} \nusername: {msg.from_user.username} \nlast name: {msg.from_user.last_name}"
        bot.send_message(valid_id[0], alert)

@bot.callback_query_handler(func=lambda call: call.data == "display")
def handle_display(call):
    bot.answer_callback_query(call.id) #required to remove the loading state, which appears upon clicking the button
    if call.message.chat.id in valid_id: #validate id
        #display total scoreboard
        text = functions.display_total_scoreboard(db.get_total_scoreboard())

        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton("Sport", callback_data="sport"), 
            telebot.types.InlineKeyboardButton("Mess", callback_data="mess")
        )        
        bot.edit_message_text(
            text= text,
            chat_id= call.message.chat.id,
            message_id= call.message.message_id,
            reply_markup= keyboard
        )

    else:
        bot.send_message(call.message.chat.id, "u do not have access to the bot, pls walk away...")

@bot.callback_query_handler(func=lambda call: call.data == "sport")
def handle_sport(call):
    bot.answer_callback_query(call.id) #required to remove the loading state, which appears upon clicking the button
    if call.message.chat.id in valid_id: #validate id
        #display sport scoreboard
        text = functions.display_sport_scoreboard(db.get_sport_scoreboard())

        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton(text="back", callback_data="display"))
        
        bot.edit_message_text(
            text= text,
            chat_id= call.message.chat.id,
            message_id= call.message.message_id,
            reply_markup= keyboard
        )

    else:
        bot.send_message(call.message.chat.id, "u do not have access to the bot, pls walk away...")

@bot.callback_query_handler(func=lambda call: call.data == "mess")
def handle_mess(call):
    bot.answer_callback_query(call.id) #required to remove the loading state, which appears upon clicking the button
    if call.message.chat.id in valid_id: #validate id
        #display mess scoreboard
        text = functions.display_mess_scoreboard(db.get_mess_scoreboard())

        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton(text="back", callback_data="display"))
        
        bot.edit_message_text(
            text= text,
            chat_id= call.message.chat.id,
            message_id= call.message.message_id,
            reply_markup= keyboard
        )

    else:
        bot.send_message(call.message.chat.id, "u do not have access to the bot, pls walk away...")

bot.polling()

# @server.route('/' + API_KEY, methods=['POST'])
# def getMessage():
#     json_string = request.get_data().decode('utf-8')
#     update = telebot.types.Update.de_json(json_string)
#     bot.process_new_updates([update])
#     return "!", 200

# @server.route("/")
# def webhook():
#     bot.remove_webhook()
#     bot.set_webhook(url="https://lckhappysquadbot.herokuapp.com/" + API_KEY)
#     return "!", 200

# if __name__ == "__main__":
#     server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
