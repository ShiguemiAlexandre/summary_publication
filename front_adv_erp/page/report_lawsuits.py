import streamlit as st
import pandas as pd
import datetime
import random

class SetPage:
    def config(self):
        st.set_page_config(
            page_title="Relatório",
            page_icon=":material/assignment:",
            layout="wide"
        )

class Sidebar:
    def render(self):
        cols = st.sidebar.columns([2, 1])
        if cols[1].button(":blue[:material/notifications:]"):
            st.write("d")

        options_selected = st.sidebar.multiselect(
            label="Processos",
            options=[
                "1501817-77.2022.8.26.0576",
                "1500276-07.2017.8.26.0019",
                "1039165-64.2015.8.26.0114"
            ]
        )
        return options_selected

class Headers:
    def render(self, options: list[str]):
        if not options:
            st.info("Seleciona ao menos um processo.")
            st.stop()

        if st.button("Download", icon=":material/download:", type="tertiary"):
            st.toast(":green[Iniciando download]", icon=":material/check:")

        tabs = st.tabs(tabs=options)
        for tab in tabs:
            firt_data_lawsuit = tab.columns([1, 1, 1])
            with firt_data_lawsuit[0]:
                st.text_input(label="Classe", value="Execução Fiscal", disabled=True, key=(random.randint(1, 100000)))
            with firt_data_lawsuit[1]:
                st.text_input(label="Vara", value="Unidade 13 - Núcleo 4.0 Execuções Fiscais Estaduais", disabled=True, key=(random.randint(1, 100000)))   
            with firt_data_lawsuit[2]:
                st.text_input(label="Valor da ação", value="R$ 10.886.834,71", disabled=True, key=(random.randint(1, 100000)))
            columns_parts = tab.columns([1, 1])
            with columns_parts[0].expander("Autor", expanded=True):
                st.write("PROCON - FUNDAÇÃO DE PROTEÇÃO E DEFESA DO CONSUMIDOR")
            with columns_parts[1].expander("Réu", expanded=True):
                st.write("Claro S.A.")

                    
            movimentos = ["Despacho", "Sentença", "Petição", "Julgamento", "Intimação", "Arquivamento", "Audiência", "Distribuição", "Citação", "Conclusão"]
            df = pd.DataFrame([
                {
                    "Data": datetime.datetime.now() - datetime.timedelta(days=i),
                    "Comentario/Movimentação": random.choice(movimentos),
                    "Selecionado": random.choice([True, False])
                }
                for i in range(10)
            ])
            tab.data_editor(df, num_rows="dynamic")
            with tab.expander("Dados do processo"):
                col_data_lawsuit = st.columns([1, 1, 1])
                with col_data_lawsuit[0]:
                    st.text_input(label="Foro", value="Foro 13 - Núcleo 4.0", disabled=True, key=(random.randint(1, 10000000)))   
                    st.text_input(label="Controle", value="2025/008072", disabled=True, key=(random.randint(1, 100000)))
                with col_data_lawsuit[1]:
                    st.text_input(label="Assunto", value="Multas e demais Sanções", disabled=True, key=(random.randint(1, 100000)))
                    st.text_input(label="Juiz", value="THAIS CAROLINE BRECHT ESTEVES", disabled=True, key=(random.randint(1, 100000)))
                with col_data_lawsuit[2]:
                    st.text_input(label="Área", value="Cível", disabled=True, key=(random.randint(1, 100000)))
                    st.text_input(label="Distribuição", value="24/07/2025 às 01:15 - Direcionada", disabled=True, key=(random.randint(1, 100000)))

SetPage().config()

options_selected = Sidebar().render()

Headers().render(options=options_selected)

