from datetime import datetime
import os
from dotenv import load_dotenv

def get_current_time():
    now = datetime.now()
    return now.strftime("Nous sommes le %d/%m/%Y et il est %H:%M")

def load_apikey():
    # Charger le fichier .env
    load_dotenv()
    return os.getenv("OPTNC_WAITINGTIME_APIKEY")
