import firebase_admin
from firebase_admin import credentials, messaging
import os

cred = (
    credentials.Certificate(
        {
            "type": "service_account",
            "project_id": os.environ["FIREBASE_PROJECT_ID"],
            "private_key_id": os.environ["FIREBASE_PRIVATE_KEY_ID"],
            "private_key": os.environ["FIREBASE_PRIVATE_KEY"].replace("\\n", "\n"),
            "client_email": os.environ["FIREBASE_CLIENT_EMAIL"],
            "client_id": os.environ["FIREBASE_CLIENT_ID"],
            "auth_uri": os.environ["FIREBASE_AUTH_URI"],
            "token_uri": os.environ["FIREBASE_TOKEN_URI"],
            "auth_provider_x509_cert_url": os.environ[
                "FIREBASE_AUTH_PROVIDER_X509_CERT_URL"
            ],
            "client_x509_cert_url": os.environ["FIREBASE_CLIENT_X509_CERT_URL"],
        }
    ),
)
firebase_admin.initialize_app(cred)


def send_fcm_message(topic, title, body):
    # Create a message to send to the device corresponding to the provided token
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        topic=topic,
    )

    # Send the message
    response = messaging.send(message)
    print("Successfully sent message:", response)
