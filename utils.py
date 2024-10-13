import streamlit as st
from datetime import datetime
import os
from dotenv import load_dotenv
import pytz
import plotly.graph_objects as go
import requests

INTERVALLE_AUTOREFRESH = 3 * 60 # 3 minutes
API_TEMPS_ATTENTE_BASE_URL = "https://api.opt.nc/temps-attente-agences/"


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

APIKEY = load_apikey()
headers = {
    "x-apikey": APIKEY,
    "Content-Type": "application/json"
}

# pas de ttl puisqu'on ne l'appel qu'une seule fois
@st.cache_data(show_spinner=False)
def fetch_communes():
    # requête pour récuperer les communes
    response_communes = requests.get(API_TEMPS_ATTENTE_BASE_URL+"communes", headers=headers)
    if response_communes.status_code == 200:
        # liste des communes
        communes = response_communes.json()
        #liste communes en MAJ
        communes_maj = [x.upper() for x in communes]
        return communes_maj
    else:
        st.error(f"Erreur lors de la récupération des communes : {response_communes.status_code}")
        return []

@st.cache_data(ttl=INTERVALLE_AUTOREFRESH, show_spinner=False)
def fetch_agences(commune):
    # requête pour récuperer agences avec la commune sélectionnée
    response_agences = requests.get(API_TEMPS_ATTENTE_BASE_URL+"agences", headers=headers, params={"commune": commune})
    if response_agences.status_code == 200:
        # liste de tout les "bâtiments" OPT
        agences = response_agences.json()
        # récupération des agences OPT
        agences_OPT = []
        for agence in agences:
            if agence["type"] in ["AGENCE", "ANNEXE"]:
                agences_OPT.append(agence)
        return agences_OPT
    else:
        st.error(f"Erreur lors de la récupération des agences : {response_agences.status_code}")
        return []

@st.cache_data(ttl=INTERVALLE_AUTOREFRESH, show_spinner=False)
def fetch_agence_by_id(id_agence):
    response = requests.get(API_TEMPS_ATTENTE_BASE_URL+f"agences/{id_agence}", headers=headers)
    if response.status_code == 200:
        agence = response.json()
        return agence
    else:
        st.error(f"Erreur lors de la récupération de l'agence {id_agence} : {response.status_code}")
        return []
