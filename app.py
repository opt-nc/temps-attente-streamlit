import streamlit as st
from streamlit_autorefresh import st_autorefresh
from utils import INTERVALLE_AUTOREFRESH, get_current_time, gauge, fetch_communes, fetch_agences, fetch_agence_by_id


st.set_page_config(page_title='Temps d\'attente en agence OPT-NC', layout = 'wide', page_icon = 'assets/images/favicon.jpg', initial_sidebar_state = 'auto')

st_autorefresh(interval=INTERVALLE_AUTOREFRESH * 1000, key="dataframerefresh")

current_time = get_current_time()
st.markdown(
    f"""
    <h1 style='text-align: center;'>{current_time}</h1>
    """, 
    unsafe_allow_html=True
)

# si aucun id n'est passé dans l'url, on ne met rien
selected_commune_param = None
selected_agence_param = None

if "idAgence" in st.query_params:
    agence = fetch_agence_by_id(st.query_params["idAgence"])
    selected_commune_param = agence["commune"]
    selected_agence_param = agence["designation"]


# Récupérer les communes (mise en cache)
communes = fetch_communes()

if communes:
    # menu déroulant pour sélection de commune
    selected_commune = st.sidebar.selectbox(
        "Sélectionnez une commune :",
        communes,
        index=communes.index(selected_commune_param) if selected_commune_param in communes else 0
        )
    
    # Récupérer les agences pour la commune sélectionnée (mise en cache)
    agences = fetch_agences(selected_commune)

    if agences:
        # Extraire le nom de l'agence 
        designation_agences = [agence["designation"] for agence in agences]

        # menu déroulant pour sélection agence
        selected_agence = st.sidebar.selectbox(
            "Sélectionnez une agence :",
            designation_agences,
            index=designation_agences.index(selected_agence_param) if selected_agence_param in designation_agences else 0
            )

        # ajout temps d'attente en texte
        for agence in agences:
            if agence["designation"]==selected_agence:
                temps_attente_agence=(agence["realAvgWaitingTimeMs"])/1000
                st.query_params["idAgence"] = agence["idAgence"]
        
        gauge(round(temps_attente_agence/60))

        st.markdown(
            f"""
            <h1 style='text-align: center;'>{selected_agence}</h1>
            """, 
            unsafe_allow_html=True
        )
        
# affichage logos partenaires
st.sidebar.image("assets/images/logo_opt.png", width=250)
st.sidebar.image("assets/images/logo_unc.jpg", width=250)

# Ajout du style et du script pour le tooltip
st.markdown("""
<style>
    [data-testid="stBaseButton-headerNoPadding"]:hover::after {
        content: "Ouvrir / Fermer";
        color: white;
    }
</style>
""", unsafe_allow_html=True)