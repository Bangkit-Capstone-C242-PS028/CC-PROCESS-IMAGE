from google.cloud import storage
import tempfile
import os

class CloudStorage:
    def __init__(self):
        self.client = storage.Client()
        self.bucket_name = os.environ["STORAGE_BUCKET_NAME"]
        self.bucket = self.client.bucket(self.bucket_name)

    def download_blob(self, source_blob_name: str) -> str:
        temp_dir = tempfile.mkdtemp()
        local_path = os.path.join(temp_dir, "image.jpg")
        
        blob = self.bucket.blob(source_blob_name)
        blob.download_to_filename(local_path)
        
        return local_path

    def upload_blob(self, local_file_path: str, destination_blob_name: str) -> str:
        blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_filename(local_file_path)
        blob.make_public()
        
        return blob.public_url

    def get_blob_path(self, patient_uid: str, lesion_id: str, processed: bool = False) -> str:
        prefix = "processed-skin-lesions" if processed else "skin-lesions"
        return f"{prefix}/{patient_uid}/{lesion_id}"