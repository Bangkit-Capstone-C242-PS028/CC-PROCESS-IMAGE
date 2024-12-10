from datetime import datetime
from src.models.skin_lesion import SkinLesionStatus
from src.services.cloud_storage import CloudStorage
from src.services.db import fetch_skin_lesion, update_lesion_status
import os
from PIL import Image
import tempfile
from src.models.preprocess import preprocess
from src.models.feature_extraction import feature_extraction
from src.models.modelling import modelling
from src.services.firebase import send_fcm_message

CLASS_DESCRIPTION_MAPPING = {
    0: "Description for class 1",
    1: "Description for class 2",
    2: "Description for class 3",
    3: "Description for class 4",
    4: "Description for class 5",
    5: "Description for class 6",
    6: "Description for class 7",
}


def process_skin_lesion(lesion_id: str):
    try:
        storage = CloudStorage()
        lesion = fetch_skin_lesion(lesion_id)

        if not lesion:
            print(f"No skin lesion found with ID: {lesion_id}")
            return

        original_blob_path = f"skin-lesions/{lesion.patientUid}/{lesion_id}"

        local_image_path = storage.download_blob(original_blob_path)
        print(local_image_path)

        image_array, image = preprocess(local_image_path)
        features = feature_extraction(image_array)
        prediction = modelling(features)

        classification = prediction[0]  # Assuming prediction is a list or array
        description = CLASS_DESCRIPTION_MAPPING.get(classification, "Unknown class")

        temp_dir = tempfile.mkdtemp()
        processed_image_path = os.path.join(temp_dir, "processed_image.jpg")
        image.save(processed_image_path)

        processed_blob_path = storage.get_blob_path(
            lesion.patientUid, lesion_id, processed=True
        )

        processed_image_url = storage.upload_blob(
            processed_image_path, processed_blob_path
        )

        update_lesion_status(
            lesion_id,
            SkinLesionStatus.COMPLETED,
            classification,
            processed_image_url,
            description,
        )

        os.remove(local_image_path)
        os.remove(processed_image_path)

        send_fcm_message(
            f"{lesion.patientUid}",
            "Skin Lesion Processed",
            f"Lesion {lesion_id} has been processed successfully.",
        )

        print(f"Successfully processed lesion {lesion_id}")

    except Exception as e:
        update_lesion_status(lesion_id, SkinLesionStatus.FAILED)
        print(f"Error processing skin lesion: {str(e)}")
