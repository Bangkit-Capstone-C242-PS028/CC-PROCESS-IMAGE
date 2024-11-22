from datetime import datetime
from db import connect_with_connector
from sqlalchemy import text
from enum import Enum

class SkinLesionStatus(str, Enum):
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'

def process_skin_lesion(lesion_id: str):
    try:
        engine = connect_with_connector()
        
        with engine.connect() as conn:
            query = text("SELECT * FROM skin_lesions WHERE id = :id")
            result = conn.execute(query, {"id": lesion_id}).fetchone()
            
            if result:
                print(f"Processing skin lesion:")
                print(f"  ID: {result.id}")
                print(f"  Patient UID: {result.patientUid}")
                print(f"  Status: {result.status}")
                print(f"  Original Image URL: {result.originalImageUrl}")
                print(f"  Created At: {result.created_at}")
                
            else:
                print(f"No skin lesion found with ID: {lesion_id}")
                
    except Exception as e:
        print(f"Error processing skin lesion: {str(e)}")