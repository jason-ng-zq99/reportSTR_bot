from typing import final
from flask import Flask
from config import TELEGRAM_BOT_TOKEN, WORKOUT_FOR_THE_WEEK
from messages import HELP_MESSAGE, EMPTY_LEADERBOARD_MESSAGE, LEADERBOARD_MESSAGE_START, SUCCESSFUL_REPORTING_MESSAGE, NO_RECORD_TO_DELETE_MESSAGE, SUCCESSFUL_DELETE_MESSAGE
from utils import convertFromGreenwichToSingaporeTime, getWeekFromDateObject, logger, createLeaderboardString
from db import is_participant_registered, add_attendance, add_participant, get_current_week_leaderboard, delete_attendance
from datetime import datetime
import telebot
import os

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
server = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, HELP_MESSAGE)
    markup = telebot.types.ReplyKeyboardMarkup(row_width=3)
    itembtn1 = telebot.types.KeyboardButton('/reportactivity')
    itembtn2 = telebot.types.KeyboardButton('/register')
    itembtn3 = telebot.types.KeyboardButton('/showleaderboard')
    itembtn4 = telebot.types.KeyboardButton('/deleteactivity')
    itembtn5 = telebot.types.KeyboardButton('/workoutfortheweek')
    itembtn6 = telebot.types.KeyboardButton('/quit')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6)
    bot.send_message(message.chat.id, "Choose one command:", reply_markup=markup)
    return

@bot.message_handler(commands=['reportactivity'])
def reportActivity(message):
    currentSingaporeTime = convertFromGreenwichToSingaporeTime(datetime.now())
    currentWeek = getWeekFromDateObject(currentSingaporeTime)
    add_attendance(currentWeek, message.from_user)

    bot.reply_to(message, SUCCESSFUL_REPORTING_MESSAGE)
    logger(f"Successfully added an activity for {message.from_user.username}")

@bot.message_handler(commands=['register'])
def register(message):
    registering_user = message.from_user
    if is_participant_registered(registering_user):
        logger(f"{registering_user.username} tried to register again.")
        bot.reply_to(message, f"You have already been registered, {registering_user.username}.")
        return

    add_participant(registering_user)
    logger(f"Successfully registered {registering_user.username}")
    bot.reply_to(message, f"You have been successfully registered, {registering_user.username}.")

@bot.message_handler(commands=['showleaderboard'])
def showleaderboard(message):
    currentWeekLeaderboard = get_current_week_leaderboard()
    if currentWeekLeaderboard is None:
        bot.reply_to(message, EMPTY_LEADERBOARD_MESSAGE)
        return 
    
    finalString = LEADERBOARD_MESSAGE_START
    for row in currentWeekLeaderboard:
        finalString += createLeaderboardString(row)
    bot.reply_to(message, finalString)
    logger(f"Successfully shown leaderboard for {message.from_user.username}")

@bot.message_handler(commands=['deleteactivity'])
def deleteactivity(message):
    currentSingaporeTime = convertFromGreenwichToSingaporeTime(datetime.now())
    currentWeek = getWeekFromDateObject(currentSingaporeTime)
    is_deleted = delete_attendance(currentWeek, message)
    if not is_deleted:
        bot.reply_to(message, NO_RECORD_TO_DELETE_MESSAGE)
        return
    
    bot.reply_to(message, SUCCESSFUL_DELETE_MESSAGE)
    logger(f"Successfully deleted an activity for {message.from_user.username}.")

@bot.message_handler(commands=['workoutfortheweek'])
def workoutfortheweek(message):
    bot.reply_to(message, WORKOUT_FOR_THE_WEEK)

@bot.message_handler(commands=['quit'])
def quit_message(message):
    bot.reply_to(message, "Nice try, theres no quitting.")
    logger(f"{message.from_user.username} tried to quit.")

def start_bot():
    print("Bot has started.")
    bot.polling()

start_bot()
