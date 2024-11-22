import base64
import json
from flask import Flask, request
from src.core.lesion import process_skin_lesion

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
        try:
            decoded_data = base64.b64decode(pubsub_message["data"]).decode("utf-8")
            message_data = json.loads(decoded_data)
            
            lesion_id = message_data.get('id')
            if lesion_id:
                process_skin_lesion(lesion_id)
            else:
                print("Error: No lesion ID provided in message")
        except Exception as e:
            print(f"Error processing message: {str(e)}")

    return ("", 204)