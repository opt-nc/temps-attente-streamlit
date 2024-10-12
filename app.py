import streamlit as st
from streamlit_autorefresh import st_autorefresh
from utils import INTERVALLE_AUTOREFRESH, get_current_time, gauge, fetch_communes, fetch_agences


st.set_page_config(page_title='Temps d\'attente en agence OPT-NC', layout = 'wide', page_icon = 'assets/images/favicon.jpg', initial_sidebar_state = 'auto')

st_autorefresh(interval=INTERVALLE_AUTOREFRESH * 1000, key="dataframerefresh")

current_time = get_current_time()
st.markdown(
    f"""
    <h1 style='text-align: center;'>{current_time}</h1>
    """, 
    unsafe_allow_html=True
)

# Récupérer les communes (mise en cache)
communes = fetch_communes()

if communes:
    # menu déroulant pour sélection de commune
    selected_commune = st.sidebar.selectbox("Sélectionnez une commune :", communes)

    # Récupérer les agences pour la commune sélectionnée (mise en cache)
    agences = fetch_agences(selected_commune)

    if agences:
        # Extraire le nom de l'agence 
        designation_agences = [agence["designation"] for agence in agences]

        # menu déroulant pour sélection agence
        selected_agence = st.sidebar.selectbox("Sélectionnez une agence :", designation_agences)

        # ajout temps d'attente en texte
        for agence in agences:
            if agence["designation"]==selected_agence:
                temps_attente_agence=(agence["realAvgWaitingTimeMs"])/1000
        
        gauge(round(temps_attente_agence/60))
        
# affichage logos partenaires
st.sidebar.image("assets/images/logo_opt.png", width=250)
st.sidebar.image("assets/images/logo_unc.jpg", width=250)
