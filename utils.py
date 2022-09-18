import sys
from config import IS_LOCAL
from datetime import datetime

def logger(message):
    if IS_LOCAL:
        print(f"[{datetime.now()}] {message}")
    else: 
        print(f"{message}")
    sys.stdout.flush()

def getCurrentWeek():
    return datetime.now().isocalendar()[1]

def createLeaderboardString(personObject):
    name = personObject['name']
    completedTimes = personObject['completedTimes']
    return f"{name}:\n" + completedTimes * "🟩 " + (7 - completedTimes) * "🟥 " + "\n\n"