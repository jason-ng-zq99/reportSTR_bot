import sys
from config import IS_LOCAL, NUMBER_OF_TIMES_A_WEEK
from datetime import datetime, timedelta

def logger(message):
    if IS_LOCAL:
        print(f"[{datetime.now()}] {message}")
    else: 
        print(f"{message}")
    sys.stdout.flush()

def getWeekFromDateObject(dateObject):
    return dateObject.isocalendar()[1]

def convertFromGreenwichToSingaporeTime(timeObject):
    return timeObject + timedelta(hours=8)

def createLeaderboardString(personObject):
    name = personObject['name']
    completedTimes = personObject['completedTimes']
    finalString = f"{name}:\n"
    finalString += (completedTimes * "🟩 ") if (completedTimes < NUMBER_OF_TIMES_A_WEEK) else (NUMBER_OF_TIMES_A_WEEK * "🟩 ")
    finalString += ((NUMBER_OF_TIMES_A_WEEK - completedTimes) * "🟥 ") if (completedTimes < NUMBER_OF_TIMES_A_WEEK) else ""
    finalString += "\n\n"
    return finalString