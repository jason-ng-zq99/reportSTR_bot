import sys
from app.config import IS_LOCAL
from datetime import datetime

def logger(message):
    if IS_LOCAL:
        print(f"[{datetime.now()}] {message}")
    else: 
        print(f"{message}")
    sys.stdout.flush()