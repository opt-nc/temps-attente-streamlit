import streamlit as st
from datetime import datetime
import os
from dotenv import load_dotenv
import pytz
import plotly.graph_objects as go


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

def gauge(temps_attente):
    plage_temps = [5, 10, 15]
    plage_couleurs = ["green", "orange", "red"]

    # Déterminer la couleur basée sur le temps d'attente
    if temps_attente <= plage_temps[0]:
        color = plage_couleurs[0]
    elif temps_attente <= plage_temps[1]:
        color = plage_couleurs[1]
    else:
        color = plage_couleurs[2]

    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = temps_attente,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Temps d'attente (minutes)"},
        gauge={
            'axis': {'range': [0, 15]},  # Plage de l'axe
            'bar': {'color': color},  # Couleur de la barre selon la plage
        }
    ))

    st.plotly_chart(fig)