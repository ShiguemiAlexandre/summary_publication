from google.cloud import firestore
from dotenv import load_dotenv
import os
import firebase_admin
from firebase_admin import credentials, firestore as admin_firestore

load_dotenv()

def get_db() -> firestore.Client:
    """
    Inicializa e retorna o cliente Firestore do Firebase.

    Returns:
        firestore.Client: Instância do Firestore.
    """
    if not firebase_admin._apps:
        cred = credentials.Certificate(os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "./config/serviceAccountKey.json"))
        firebase_admin.initialize_app(cred)

    return admin_firestore.client()
