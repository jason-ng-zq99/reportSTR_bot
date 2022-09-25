import sys
from config import IS_LOCAL
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
    finalString += (completedTimes * "🟩 ") if (completedTimes < 7) else (7 * "🟩 ")
    finalString += ((7 - completedTimes) * "🟥 ") if (completedTimes < 7) else ""
    finalString += "\n\n"
    return finalString