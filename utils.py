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
    return f"{name}:\n" + completedTimes * "🟩 " + (7 - completedTimes) * "🟥 " + "\n\n"