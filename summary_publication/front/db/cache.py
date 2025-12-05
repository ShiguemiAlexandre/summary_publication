from google.cloud.firestore import CollectionReference, DocumentReference
from db import get_db

from datetime import datetime

class CacheCollectionRef:
    """
    Fornece uma referência à coleção 'cache' no Firestore.

    Essa coleção é usada para armazenar dados temporários, como IDs de publicações
    processadas por data, para evitar reprocessamentos.
    """
    def __init__(self):
        self.db = get_db()

    def get(self) -> CollectionReference:
        """
        Retorna a referência da coleção 'cache'.

        Returns:
            CollectionReference: Referência à coleção 'cache'.
        """
        return self.db.collection("cache")

class PublicationDateDocumentRef:
    """
    Fornece uma referência a um documento dentro da coleção 'cache' com base na data.

    Cada documento é identificado por uma data (string) e pode armazenar os IDs de publicações
    processadas naquele dia.
    """
    def __init__(self):
        self.cache_ref = CacheCollectionRef()
    
    def get(self, date: str) -> DocumentReference:
        """
        Retorna a referência a um documento da coleção 'cache' para a data fornecida.

        Args:
            date (str): A data usada como ID do documento (ex: '2025-08-02').

        Returns:
            DocumentReference: Referência ao documento correspondente à data.
        """
        ref_document_date = self.cache_ref.get().document(date)
        if not ref_document_date.get().exists:
            ref_document_date.set({"create_at": datetime.now().isoformat()})

        return ref_document_date

class IDPublicationCollectionRef:
    """
    Fornece uma referência a uma coleção dentro do documento com base no ID.
    """
    def __init__(self):
        self.publication_date_document = PublicationDateDocumentRef()

    def get(self, id: str, date: str) -> CollectionReference:
        """
        Retorna a referência da coleção por ID.

        Returns:
            CollectionReference: Referência à coleção ID.
        """
        return self.publication_date_document.get(date=date).collection(str(id))
