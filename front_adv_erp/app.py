import streamlit as st

pages = [
    st.Page("page/home.py", title="Home", icon=":material/home:"),
    st.Page("page/report_lawsuits.py", title="Gerenciar processos", icon=":material/assignment:")
]

st.logo("./img/logo.png", size="large", icon_image="./img/logo.png")

pg = st.navigation(pages, position="top")

st.image("./img/japantech.png")

pg.run()