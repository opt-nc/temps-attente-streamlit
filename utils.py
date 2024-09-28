from datetime import datetime
import os
from dotenv import load_dotenv
import pytz

# Fixer le fuseau horaire de la Nouvelle-Calédonie
ncl_tz = pytz.timezone('Pacific/Noumea')

# Obtenir la datetime dans le fuseau horaire de NC
def get_current_time():
    ncl_time = datetime.now(ncl_tz)
    return ncl_time.strftime("Nous sommes le %d/%m/%Y et il est %H:%M")

def load_apikey():
    # Charger le fichier .env
    load_dotenv()
    return os.getenv("OPTNC_WAITINGTIME_APIKEY")
