from flask import Flask, request
from app.config import TELEGRAM_BOT_TOKEN
from app.messages import help_message
from app.utils import logger
from app.db import add_attendance, add_participant
from datetime import datetime
import telebot
import os

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
app = Flask(__name__)

@app.route('/' + TELEGRAM_BOT_TOKEN, methods=['POST'])
def getMessage():
   bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
   return "!", 200
@app.route("/")
def webhook():
   bot.remove_webhook()
   bot.set_webhook(url='<HEROKU Web URL>' + TELEGRAM_BOT_TOKEN)
   return "!", 200

@bot.message_handler(commands=['start', 'help'])
def help(message):
    bot.reply_to(message, help_message)
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = telebot.types.KeyboardButton('/reportactivity')
    itembtn2 = telebot.types.KeyboardButton('/register')
    itembtn3 = telebot.types.KeyboardButton('/showleaderboard')
    itembtn4 = telebot.types.KeyboardButton('/quit')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    bot.send_message(message.chat.id, "Choose one command:", reply_markup=markup)
    return

@bot.message_handler(commands=['quit'])
def quit_message(message):
    bot.reply_to(message, "Nice try, theres no quitting.")
    logger(f"{message.from_user.username} tried to quit.")

@bot.message_handler(commands=['register'])
def register(message):
    registering_user = message.from_user
    add_participant(registering_user)
    logger(f"Successfully registered {registering_user.username}")
    bot.reply_to(message, f"You have been successfully registered, {registering_user.username}.")

@bot.message_handler(commands=['reportactivity'])
def reportActivity(message):
    currentWeek = datetime.now().isocalendar()[1]
    add_attendance(currentWeek, message.from_user)

def start_bot():
    logger("Bot has started.")
    bot.polling()

if __name__ == "__main__":
   bot.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))