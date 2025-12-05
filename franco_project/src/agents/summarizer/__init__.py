from astrea.api.publication.clippings import ClippingsQuery
from astrea.api.login import Login
from gemini.credencials import Credencials
from gpt import GPTOpenAI

from db.cache import IDPublicationCollectionRef
from db.publication import FirestorePublicationPaths
from src.agents.sender_email import SenderEmail

from db.prompt import PromptsRefsFirestore
from db import get_db

import logging
from google.cloud.firestore_v1 import ArrayUnion
from datetime import datetime
import pandas as pd
from io import BytesIO
import time
import json

class PromptNotFound(Exception):
    """
    Prompt não foi encontrado
    """

class PublicationTextNotFound(Exception):
    """
    Texto de publicação não encontrado
    """

class IDPublicationNotFound(Exception):
    """
    ID da publicação não foi encontrado
    """

class SummaryPublication:
    def __init__(self, system_name: str, client_name: str):
        self.system_name: str = system_name
        self.client_name: str = client_name

        self.credentials_astrea = Login().post()
        self.sender_email = SenderEmail()
        self.TOKEN = self.credentials_astrea.get("session", "")

        self.clippings_query = ClippingsQuery(token=self.TOKEN)
        self.gemini_credencials = Credencials()
        self.gpt = GPTOpenAI()
        self.logger = logging.getLogger(__name__)

        self.db = get_db()
        self.batch = self.db.batch()

        self.cache_publication_id_ref = IDPublicationCollectionRef()
        self.publication_id_ref = FirestorePublicationPaths()

        self.ref_prompt = PromptsRefsFirestore()

        self.data_df = []
    
    def _get_prompt(self) -> str:
        return self.ref_prompt.get_last_prompt_created(
            name_client=self.client_name,
            type_system=self.system_name
        )

    def _get_value(self, lst, idx):
        return lst[idx] if len(lst) > idx else ""

    def _create_sheet(self) -> bytes:
        self.logger.info("Criando planilha do excel")

        df = pd.DataFrame(self.data_df)

        excel_buffer = BytesIO()

        df.to_excel(excel_buffer, index=False)

        excel_buffer.seek(0)

        return excel_buffer.read()

    def _commit_update_status_publication(self):
        if not self.data_df:
            return

        for publication in self.data_df:
            publcation_id = publication.get("data_default").get("id")
            ref = self.publication_id_ref.publications_by_id(
                client_name=self.client_name,
                system=self.system_name,
                document_id=str(publcation_id)
            )

            self.batch.update(
                reference=ref,
                field_updates={
                    "email_sent": True
                }
            )

    def _publication_captured(self, id: str) -> bool:
        ref = self.publication_id_ref.publications_by_id(
            client_name=self.client_name,
            system=self.system_name,
            document_id=id
        )

        if ref.get().exists:
            return True

        return False
    
    def astrea_clippings(self):
        astrea_result = self.clippings_query.query_post()

        clippings = astrea_result.get("clippings", "")

        if not clippings:
            self.logger.warning("Não foi encontrado nenhuma publicação")
            self.sender_email.send(df=b"", quantity=0)
            return None
        
        return clippings

    def generate(self):
        clippings = self.astrea_clippings()
        
        model = self.gemini_credencials.login()

        count = 0

        self.logger.info(f"Iniciando resumo de publicações, quantidade: {len(clippings)}")
        for publication in clippings:
            if self._publication_captured(id=str(publication.get("id"))):
                self.logger.info(f"Processo {publication.get('clippingLawsuitNumber')}, já foi resumido ID: {str(publication.get('id'))}")
                continue

            started = datetime.now()
            count += 1
            self.logger.info(f"Resumindo: CNJ: {publication.get('clippingLawsuitNumber', '')}, Fila: {count}")

            text = publication.get("clippingMatter", "")
            if not text:
                raise PublicationTextNotFound()
            
            prompt_with_publication = f"{self._get_prompt().get()[0].to_dict()['prompt']}, Texto: {publication.get('clippingMatter')}"

            result_gemini = model.generate_content(prompt_with_publication)

            result_splited = result_gemini.text.replace("```json", "").replace("```", "").strip()
            result_json = json.loads(result_splited)

            date_now = datetime.now()

            id_publication = publication.get("id", "")

            if not id_publication:
                raise IDPublicationNotFound()

            ref_cache = self.cache_publication_id_ref.get(date=date_now.strftime("%Y-%m-%d"), id=id_publication)

            ref_document_cache = ref_cache.document()

            document_id_ref_cache = ref_document_cache.id

            publication_ref = self.publication_id_ref.publications(client_name=self.client_name, system=self.system_name)
            publication_snapshot = publication_ref.document(str(id_publication))

            if publication_snapshot.get().exists:
                publication_snapshot.update(
                    {
                        "data_default": publication,
                        "last_edited_at": datetime.now().isoformat(),
                        "summary_craw": result_gemini.text,
                        "summary_splited": result_splited,
                        "summary_json": result_json,
                        # "email_sent": False,
                        "cache_id": ArrayUnion([{document_id_ref_cache: datetime.now().isoformat()}]),
                        "system": self.system_name
                    }
                )
            else:
                publication_snapshot.set(
                    {
                        "data_default": publication,
                        "create_at": datetime.now().isoformat(),
                        "summary_craw": result_gemini.text,
                        "summary_splited": result_splited,
                        "summary_json": result_json,
                        "email_sent": False,
                        "cache_id": [{document_id_ref_cache: datetime.now().isoformat()}],
                        "system": self.system_name
                    }
                )

            ref_document_cache.set(
                {
                    "data_default": publication,
                    "create_at": datetime.now().isoformat(),
                    "summary_craw": result_gemini.text,
                    "summary_splited": result_splited,
                    "summary_json": result_json,
                    "duration": (datetime.now() - started).total_seconds(),
                    "system": self.system_name,
                    "prompt_default": prompt_with_publication

                }
            )

            self.data_df.append(
                {
                    "Número do Processo": result_json.get("numero_processo"),
                    "Data da Publicação": result_json.get("data_publicacao"),
                    "Data de Divulgação": result_json.get("data_divulgacao"),
                    "Prazo": result_json.get("prazo"),
                    "Prazo Fatal": result_json.get("prazo_fatal"),
                    "Prazo Antecipado": result_json.get("prazo_antecipado"),
                    "Tarefa": result_json.get("tarefa"),
                    "Evento / Audiência": result_json.get("evento_audiencia"),
                    "Observações": result_json.get("observacoes"),
                    "Duplicidade": result_json.get("duplicidade"),
                    "create_at": datetime.now().isoformat(),
                    "summary_craw": result_gemini.text,
                    "summary_splited": result_json,          # agora o próprio JSON
                    "data_default": publication,
                    "publication_ID": str(id_publication),
                    "document_id_db": document_id_ref_cache,
                    "duration": (datetime.now() - started).total_seconds(),
                }
            )

        self.logger.info("Montando email para ser enviado")

        self._commit_update_status_publication()

        bytes_excel = self._create_sheet()

        self.sender_email.send(df=bytes_excel, quantity=len(self.data_df))

        self.batch.commit()
        self.logger.info("Status das publicações foi alterados")

        time.sleep(10)

        self.db.close()