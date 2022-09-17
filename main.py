from tracemalloc import start
from flask import Flask
from config import TELEGRAM_BOT_TOKEN
from messages import help_message
from utils import logger
from db import add_participant
import telebot

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
server = Flask(__name__)

@bot.message_handler(commands=['start', 'help'])
def help(message):
    bot.reply_to(message, help_message)
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = telebot.types.KeyboardButton('/help')
    itembtn2 = telebot.types.KeyboardButton('/register')
    itembtn3 = telebot.types.KeyboardButton('/update')
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

def start_bot():
    print("Bot has started.")
    bot.polling()

start_bot()