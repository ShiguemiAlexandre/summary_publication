from datetime import datetime, time
from typing import Union

from google.cloud.firestore import CollectionReference, DocumentReference, FieldFilter
from db import get_db


class FirestorePublicationPaths:
    """
    Fornece métodos para acessar referências da coleção 'publication' no Firestore.

    Estrutura:
    publication/
        clients/
            {cliente}/
                systems/
                    {sistema}/
                        {publicações}
    """

    def __init__(self):
        self.db = get_db()
        self.root = self.db.collection("publication")

    def clients_doc(self) -> DocumentReference:
        """Retorna o documento raiz 'clients', criando se não existir."""
        ref = self.root.document("clients")
        if not ref.get().exists:
            ref.set({"created_at": datetime.utcnow().isoformat()})
        return ref

    def client_collection(self, client_name: str) -> CollectionReference:
        """Retorna a subcoleção de um cliente."""
        return self.clients_doc().collection(client_name)

    def systems_doc(self, client_name: str) -> DocumentReference:
        """Retorna o documento 'systems' de um cliente."""
        return self.client_collection(client_name).document("systems")

    def system_collection(self, client_name: str, system: str) -> CollectionReference:
        """Retorna a coleção de publicações de um sistema."""
        return self.systems_doc(client_name).collection(system)

    def publications(self, client_name: str, system: str) -> CollectionReference:
        """Retorna as publicações de um cliente/sistema."""
        return self.system_collection(client_name, system)

    def publications_by_id(self, client_name: str, system: str, document_id: str) -> DocumentReference:
        """Retorna um determinado document da collection"""
        return self.system_collection(client_name, system).document(document_id)

    def publications_filtred(
            self,
            client_name: str,
            system: str,
            start_date: datetime,
            end_date: datetime,
            lawsuit_number: str = None,
            publication_id: str = None
        ):
        start_date_str = datetime.combine(start_date, time.min).strftime("%Y-%m-%dT%H:%M:%S.%f")
        end_date_str = datetime.combine(end_date, time.max).strftime("%Y-%m-%dT%H:%M:%S.%f")

        ref = self.system_collection(client_name, system).where(
            "create_at", ">=", start_date_str
        ).where(
            "create_at", "<=", end_date_str
        )
        if lawsuit_number:
            ref = ref.where(
                filter=FieldFilter(
                    field_path="data_default.lawsuitNumber",
                    op_string="==",
                    value=lawsuit_number
                )
            )
        
        if publication_id:
            ref = ref.where(
                filter=FieldFilter(
                    field_path="data_default.id",
                    op_string="==",
                    value=publication_id
                )
            )

        return ref
