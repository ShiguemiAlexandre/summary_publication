import streamlit as st
from datetime import date, timedelta, datetime
from model.system import System
from db.publication import FirestorePublicationPaths

class Settings:
    def configure(self):
        st.set_page_config(
            page_title="Gerenciar publicações",
            layout="wide"
        )

    def previous_business_day(self, current_date=None) -> datetime:
        if current_date is None:
            current_date = date.today()
        day = current_date - timedelta(days=1)
        while day.weekday() >= 5:
            day -= timedelta(days=1)
        return day


class Header:
    def render(self):
        st.subheader("Gerenciar publicações", divider=True)

        datetime_now: datetime = datetime.now()

        yesterday: datetime = Settings().previous_business_day()

        column_date, column_system, column_id = st.columns([1, 1, 1])

        with column_date:
            start_date, end_date = st.date_input(
                "Data", value=(yesterday, datetime_now)
            )
        
        with column_system:
            system = st.multiselect(
                "Sistema",
                options=System.ALL_SYSTEMS.value,
                max_selections=1,
                placeholder="Selecione o sistema",
            )

        with column_id:
            publication_id = st.text_input(label="Publicação ID")

        column_name, column_lawsuit = st.columns([2, 1])
        
        with column_name:
            name_client = st.text_input("Nome do cliente", value="franco")
        
        with column_lawsuit:
            lawsuit_number = st.text_input(label="Número do processo", placeholder="Processo", value="0010571-11.2025.5.15.0099")

        st.divider()

        return start_date, end_date, system, name_client, lawsuit_number, publication_id


class Body:
    def __init__(self):
        self.ref_publication = FirestorePublicationPaths()
    
    def row_publication(self, publication_data):
        raw_data: dict = publication_data.to_dict()
        publication_default = raw_data["data_default"]
        lawsuit_number: str = str(publication_default.get("lawsuitNumber", "Sem número"))
        publication: str = str(publication_default.get(
            "clippingMatter",
            "Nenhum texto encontrado favor informar o suporte do processo"
        ))
        summary_publication: str = raw_data.get("summary_craw", "Sem resumo")
    
        with st.expander(lawsuit_number):
            columns_id, _ = st.columns([1, 3])
            columns_id.text(f"Publicação ID: {publication_default.get("id", "ID não encontrado")}")
            st.text_area(label="Publicação", value=publication, height="content")
            st.text_area(label="Resumo", value=summary_publication, height="content")


    def render(self, name_client, system, start_date: datetime, end_date: datetime, lawsuit_number: str, publication_id: str):
        if not system:
            st.warning("Selecione o sistema que deseja consultar")
            st.stop()
        
        if not name_client:
            st.warning("Selecione um cliente")
            st.stop()

        blobs = self.ref_publication.publications_filtred(
            client_name=name_client,
            system=system[0],
            start_date=start_date,
            end_date=end_date,
            lawsuit_number=lawsuit_number,
            publication_id=publication_id
        )

        for blob in blobs.stream():
            self.row_publication(publication_data=blob)


class PublicationPage:
    def render(self):
        Settings().configure()
        start_date, end_date, system, name_client, lawsuit_number, publication_id = Header().render()
        Body().render(name_client, system, start_date, end_date, lawsuit_number, publication_id)


PublicationPage().render()