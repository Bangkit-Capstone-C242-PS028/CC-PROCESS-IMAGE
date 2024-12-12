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
from src.models.grad_cam import image_grad_cam
from src.services.firebase import send_fcm_message

CLASSIFICATION_MAPPING = {
    0: "Actinic keratoses and intraepithelial carcinoma",
    1: "basal cell carcinoma",
    2: "benign keratosis-like lesions",
    3: "dermatofibroma ",
    4: "melanoma",
    5: "melanocytic nevi",
    6: "vascular lesions",
}

CLASS_DESCRIPTION_MAPPING = {
    0: "This is a precancerous skin condition that can develop into skin cancer if not treated.",
    1: "This is a type of skin cancer that originates in the basal cells, which are located in the lower part of the epidermis.",
    2: "These are noncancerous skin growths that may resemble warts or skin tags.",
    3: "This is a common, benign skin growth that usually appears as a firm, red or brown bump.",
    4: "This is a type of skin cancer that develops from melanocytes, the cells that produce melanin.",
    5: "These are commonly known as moles and are benign growths of melanocytes.",
    6: "These are abnormalities of the blood vessels in the skin, such as cherry angiomas or spider veins.",
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

        image_array = preprocess(local_image_path)
        features = feature_extraction(image_array)
        prediction = modelling(features)
        image = image_grad_cam(local_image_path)

        classification = CLASSIFICATION_MAPPING.get(prediction[0], "Unknown class")
        description = CLASS_DESCRIPTION_MAPPING.get(prediction[0], "Unknown class")

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
