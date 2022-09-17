from firebase_admin import credentials, firestore, initialize_app
from time import time
import config

cred = credentials.Certificate(
    {
        "type": config.DB_TYPE,
        "project_id": config.DB_PROJECT_ID,
        "private_key_id": config.DB_PRIVATE_KEY_ID,
        "private_key": config.DB_PRIVATE_KEY,
        "client_email": config.DB_CLIENT_EMAIL,
        "client_id": config.DB_CLIENT_ID,
        "auth_uri": config.DB_AUTH_URI,
        "token_uri": config.DB_TOKEN_URI,
        "auth_provider_x509_cert_url": config.DB_AUTH_PROVIDER_X509_CERT_URL,
        "client_x509_cert_url": config.DB_CLIENT_X509_CERT_URL
    }
)
initialize_app(cred)
db = firestore.client()

def add_participant(participant):
    doc_ref = db.collection('Participants').document(str(participant.id))
    doc_ref.set({
        "id" : str(participant.id),
        "name" : participant.username,
        "registered_date" : time(),
        "last_update_time" : time(),
    })

