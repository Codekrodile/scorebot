import telebot
import mongodatabase
import functions

import config
API_KEY = config.API_KEY
valid_id = [int(id) for id in config.VALID_ID.split(';')]

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])
def start(msg):
    #validate id
    if msg.chat.id in valid_id:
        # functions.save_record(msg) #record log for testing purpose

        text = "welcome to schedulyser! click the button below to get started:)"

        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(telebot.types.InlineKeyboardButton("menu", callback_data="menu"))

        bot.send_message(msg.chat.id, text, reply_markup=keyboard)
    
    else:
        bot.send_message(msg.chat.id, "u do not have access to the bot, pls walk away...")
        alert = f"id entry at start command \nuser id: {msg.from_user.id} \nis_bot: {msg.from_user.is_bot} \nfirst name: {msg.from_user.first_name} \nusername: {msg.from_user.username} \nlast name: {msg.from_user.last_name}"
        bot.send_message(valid_id[0], alert)

@bot.callback_query_handler(func=lambda call: call.data == "menu")
def handle_menu(call):
    bot.answer_callback_query(call.id) #required to remove the loading state, which appears upon clicking the button

    #validate id
    if call.message.chat.id in valid_id:
        # functions.save_record(call) #record log for testing purpose
        text = "menu \n\ninsert random menu text"

        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton("button1", callback_data=f"nowhere"), 
            telebot.types.InlineKeyboardButton("button2", callback_data="nowhere"),
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


bot.polling()
