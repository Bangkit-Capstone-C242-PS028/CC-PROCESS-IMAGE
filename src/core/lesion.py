from datetime import datetime
from src.models import SkinLesionStatus
from src.services.cloud_storage import CloudStorage
from src.services.db import fetch_skin_lesion, update_lesion_status
import os
from PIL import Image
import tempfile

def format_lesion_details(lesion) -> str:
    return "\n".join([
        "Processing skin lesion:",
        f"  ID: {lesion.id}",
        f"  Patient UID: {lesion.patientUid}",
        f"  Status: {lesion.status}",
        f"  Original Image URL: {lesion.originalImageUrl}",
        f"  Created At: {lesion.createdAt}",
        f"  Processed At: {lesion.processedAt if lesion.processedAt else 'Not processed'}"
    ])

def process_skin_lesion(lesion_id: str):
    try:
        storage = CloudStorage()
        lesion = fetch_skin_lesion(lesion_id)
        
        if not lesion:
            print(f"No skin lesion found with ID: {lesion_id}")
            return
            
        print(format_lesion_details(lesion))
        
        original_blob_path = f"skin-lesions/{lesion.patientUid}/{lesion_id}"
        
        local_image_path = storage.download_blob(original_blob_path)
        print(f"Downloaded blob to {local_image_path}")
        
        temp_dir = tempfile.mkdtemp()
        processed_image_path = os.path.join(temp_dir, "processed_image.jpg")
        Image.open(local_image_path).save(processed_image_path)
        
        processed_blob_path = storage.get_blob_path(lesion.patientUid, lesion_id, processed=True)
        processed_image_url = storage.upload_blob(processed_image_path, processed_blob_path)
        
        update_lesion_status(
            lesion_id, 
            SkinLesionStatus.COMPLETED,
            "NORMAL",  # Mock classification
            processed_image_url
        )
        
        os.remove(local_image_path)
        os.remove(processed_image_path)
        
        print(f"Successfully processed lesion {lesion_id}")
        print(f"Classification: NORMAL")
        print(f"Processed image URL: {processed_image_url}")
        
    except Exception as e:
        print(f"Error processing skin lesion: {str(e)}")
        update_lesion_status(lesion_id, SkinLesionStatus.FAILED)