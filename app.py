import streamlit as st
from streamlit_autorefresh import st_autorefresh
from utils import load_apikey, get_current_time

st.set_page_config(page_title='Temps d\'attente en agence OPT-NC', layout = 'wide', page_icon = 'assets/images/favicon.jpg', initial_sidebar_state = 'auto')

st_autorefresh(interval=2 * 60 * 1000, key="dataframerefresh")

apikey = load_apikey()

st.write("Hello OPT-NC")

current_time = get_current_time()
st.write(current_time)

st.image("assets/images/logo_opt.png", width=250)
st.image("assets/images/logo_unc.jpg", width=250)