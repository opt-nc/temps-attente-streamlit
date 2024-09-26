import streamlit as st
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title='Hello OPT NC', layout = 'wide', page_icon = 'assets/images/favicon.jpg', initial_sidebar_state = 'auto')

st_autorefresh(interval=2 * 60 * 1000, key="dataframerefresh")


st.write("Hello OPT-NC")

now = datetime.now()
formatted_date_time = now.strftime("Nous sommes le %d/%m/%Y et il est %H:%M")
st.write(formatted_date_time)

st.image("assets/images/logo_opt.png", width=250)
st.image("assets/images/logo_unc.jpg", width=250)