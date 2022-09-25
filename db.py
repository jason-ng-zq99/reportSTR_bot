from datetime import datetime
from firebase_admin import credentials, firestore, initialize_app
from time import time
from utils import convertFromGreenwichToSingaporeTime, logger, getWeekFromDateObject
import config as config

cred = credentials.Certificate({
        "type": config.DB_TYPE,
        "project_id": config.DB_PROJECT_ID,
        "private_key_id": config.DB_PRIVATE_KEY_ID,
        "private_key": config.DB_PRIVATE_KEY,
        "client_email": config.DB_CLIENT_EMAIL,
        "client_id": config.DB_CLIENT_ID,
        "auth_uri": config.DB_AUTH_URI,
        "token_uri": config.DB_TOKEN_URI,
        "auth_provider_x509_cert_url": config.DB_AUTH_PROVIDER_X509_CERT_URL,
        "client_x509_cert_url": config.DB_CLIENT_X509_CERT_URL
    }
)
initialize_app(cred)
db = firestore.client()

def add_participant(participant):
    doc_ref = db.collection('Participants').document(str(participant.id))
    doc_ref.set({
        "id" : str(participant.id),
        "name" : participant.username,
        "registered_date" : time(),
        "last_update_time" : time(),
    })
    
    currentSingaporeWeek = getWeekFromDateObject(convertFromGreenwichToSingaporeTime(datetime.now()))
    doc_ref = db.collection('WeeklyAttendance').document(str(currentSingaporeWeek))
    if not doc_ref.get().exists:
        doc_ref.set({
            "week": currentSingaporeWeek
        })
    
    doc_ref = doc_ref.collection('AttendanceList').document(str(participant.id))
    doc_ref.set({
        "participantId" : str(participant.id),
        "participantName" : participant.username,
        "completedTimes" : 0
    })

def is_participant_registered(participant):
    doc_ref = db.collection('Participants').document(str(participant.id))
    return doc_ref.get().exists

def get_all_participants():
    doc_ref = db.collection('Participants').stream()
    return doc_ref.get().to_dict()

def add_attendance(week, participant, times=1):
    doc_ref = db.collection('WeeklyAttendance').document(str(week))
    if not doc_ref.get().exists:
        doc_ref.set({
            "week": week
        })

    doc_ref = doc_ref.collection('AttendanceList').document(str(participant.id))
    if not doc_ref.get().exists:
        doc_ref.set({
            "participantId" : str(participant.id),
            "participantName" : participant.username,
            "completedTimes" : 0
        })
        return 

    currentCompletedTimes = doc_ref.get().to_dict()['completedTimes']
    newCompletedTimes = currentCompletedTimes + times

    doc_ref.update({
        "completedTimes" : newCompletedTimes if newCompletedTimes <= 7 else 7
    })

def delete_attendance(week, participant, times=1):
    doc_ref=db.collection('WeeklyAttendance').document(str(week))
    if not doc_ref.get().exists:
        logger(f"{week} has no activities yet..")
        return False
    
    doc_ref = doc_ref.collection('AttendanceList').document(str(participant.id))
    if not doc_ref.get().exists:
        logger(f"{participant.username} does not have any activity for week {week}.")
        return False

    currentCompletedTimes = doc_ref.get().to_dict()['completedTimes']
    if currentCompletedTimes < 1:
        logger(f"{participant.username} only completed {currentCompletedTimes} workouts this week; unable to delete attendance.")
        return False
    
    doc_ref.update({
        "completedTimes" : currentCompletedTimes - times
    })

    return True


def get_current_week_leaderboard():
    currentGreenwichTime = datetime.now()
    currentSingaporeTime = convertFromGreenwichToSingaporeTime(currentGreenwichTime)
    currentWeek = getWeekFromDateObject(currentSingaporeTime)

    doc_ref = db.collection('WeeklyAttendance').document(str(currentWeek))
    if not doc_ref.get().exists:
        return None

    doc_ref = doc_ref.collection('AttendanceList').stream()
    attendanceList = []
    for rows in doc_ref:
        tempDict = rows.to_dict()
        name = tempDict['participantName']
        completedTimes = tempDict['completedTimes']

        attendanceList.append({
            'name': name,
            "completedTimes": completedTimes
        })

    return attendanceList
