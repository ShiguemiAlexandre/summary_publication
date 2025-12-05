from google.cloud.firestore_v1 import CollectionReference, DocumentReference
from google.cloud import firestore
from datetime import datetime

from db import get_db

class DataEmpty(Exception):
    """
    Dados está vazio
    """

class PromptsRefsFirestore:
    def __init__(self):
        self.db = get_db()
        self.root = self.db.collection("prompt")

    def clients_docs(self, name_client: str) -> DocumentReference:
        return self.root.document(name_client)
    
    def system_client_collection(self, name_client: str, type_system: str) -> CollectionReference:
        return self.clients_docs(name_client=name_client).collection(type_system)
    
    def get_last_prompt_created(self, name_client: str, type_system: str) -> DocumentReference:
        ref = self.system_client_collection(name_client=name_client, type_system=type_system)

        return ref.order_by(
            field_path="created_at",
            direction=firestore.Query.DESCENDING
        ).limit(1)

    def create_new_prompt(self, name_client: str, type_system: str, **kwargs) -> bool:
        """
        Cria um documento no path '/prompt/client/system/'

        Exceptions:
            
        """
        if not kwargs:
            raise DataEmpty()

        ref = self.system_client_collection(name_client=name_client, type_system=type_system)

        kwargs.update(
            {
                "created_at": datetime.now().isoformat()
            }
        )

        ref.document().set(kwargs)

        return True