import base64
import json
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["POST"])
def index():
    envelope = request.get_json()
    print(f"Received envelope: {envelope}")
    
    if not envelope:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        return f"Bad Request: {msg}", 400

    pubsub_message = envelope["message"]


    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        # Decode the base64 message
        decoded_data = base64.b64decode(pubsub_message["data"]).decode("utf-8")
        message_data = json.loads(decoded_data)
        
        # Log the specific fields we expect
        print("Received skin lesion data:")
        print(f"  ID: {message_data.get('id')}")
        print(f"  Patient UID: {message_data.get('patientUid')}")
        print(f"  File Name: {message_data.get('fileName')}")
        print(f"  Created At: {message_data.get('createdAt')}")

    return ("", 204)