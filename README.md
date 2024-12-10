# Skin Lesion Processing and Classification

This project processes and classifies skin lesion images using a machine learning model. The project is designed to be deployed on Google Cloud Run and integrates with Firebase for notifications and Google Cloud Storage for storing images.

## Overview

The project performs the following steps:
1. Downloads a skin lesion image from Google Cloud Storage.
2. Preprocesses the image to match the input requirements of the machine learning model.
3. Extracts features from the image using a pre-trained model.
4. Classifies the image using a machine learning model.
5. Maps the classification to a human-readable description.
6. Updates the lesion status and classification in the database.
7. Sends a notification via Firebase Cloud Messaging (FCM) to a specified topic.

## Project Structure

```
DERMASCAN-ML-API
├── Dockerfile
├── flake.lock
├── flake.nix
├── README.md
├── requirements.txt
└── src/
    ├── core/
    │   └── lesion.py
    ├── main.py
    ├── models/
    │   ├── best_xgb_model_r50.pkl
    │   ├── feature_extraction.py
    │   ├── modelling.py
    │   ├── preprocess.py
    │   └── skin_lesion.py
    └── services/
        ├── cloud_storage.py
        ├── db.py
        └── firebase.py
```

## Setup

### Prerequisites

- Python 3.11
- Google Cloud SDK
- Firebase project with service account credentials
- Google Cloud Storage bucket
- Google Cloud SQL instance

### Environment Variables

Create a `.env` file in the root directory with the following content:

```
INSTANCE_UNIX_SOCKET=
DB_USER=
DB_PASS=
DB_NAME=
STORAGE_BUCKET_NAME=
FIREBASE_PROJECT_ID=
FIREBASE_PRIVATE_KEY_ID=
FIREBASE_PRIVATE_KEY=
FIREBASE_CLIENT_EMAIL=
FIREBASE_CLIENT_ID=
FIREBASE_AUTH_URI=
FIREBASE_TOKEN_URI=
FIREBASE_AUTH_PROVIDER_X509_CERT_URL=
FIREBASE_CLIENT_X509_CERT_URL=
FIREBASE_UNIVERSE_DOMAIN=
```

### Install Dependencies

```sh
pip install -r requirements.txt
```

### Initialize Firebase Admin SDK

Ensure you have the Firebase service account key JSON file and set the path in the `.env` file.

### Deploy to Google Cloud Run

1. **Create a service account for Cloud Run Pub/Sub Invoker:**

```sh
gcloud iam service-accounts create cloud-run-pubsub-invoker \
    --display-name "Cloud Run Pub/Sub Invoker"
```

2. **Add IAM policy binding to allow Pub/Sub to invoke the Cloud Run service:**

```sh
gcloud run services add-iam-policy-binding pubsub-tutorial \
    --member=serviceAccount:cloud-run-pubsub-invoker@PROJECT_ID.iam.gserviceaccount.com \
    --role=roles/run.invoker
```

3. **Build and deploy the service:**

```sh
gcloud builds submit --tag gcr.io/PROJECT_ID/skin-lesion-service
gcloud run deploy skin-lesion-service --image gcr.io/PROJECT_ID/skin-lesion-service --platform managed
```

### Bind to a Pub/Sub Topic

1. **Create a Pub/Sub topic:**

```sh
gcloud pubsub topics create skin-lesion-topic
```

2. **Create a Pub/Sub subscription:**

```sh
gcloud pubsub subscriptions create skin-lesion-subscription --topic=skin-lesion-topic
```

3. **Bind the Pub/Sub topic to the Cloud Run service:**

```sh
gcloud run services add-iam-policy-binding skin-lesion-service \
    --member=serviceAccount:cloud-run-pubsub-invoker@PROJECT_ID.iam.gserviceaccount.com \
    --role=roles/run.invoker
```

## Usage

### Endpoint

The service exposes a single endpoint `/` which listens for Pub/Sub messages. The message should contain the `lesion_id` of the skin lesion to be processed.

### Example Pub/Sub Message

```json
{
  "message": {
    "data": "eyJpZCI6ICIxMjM0NTY3ODkwIn0="  # Base64 encoded JSON with lesion_id
  }
}
```