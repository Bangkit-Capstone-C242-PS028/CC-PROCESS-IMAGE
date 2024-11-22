import os
import sqlalchemy
from sqlalchemy import text
from datetime import datetime


def connect_unix_socket() -> sqlalchemy.engine.base.Engine:
    """Initializes a Unix socket connection pool for a Cloud SQL instance of MySQL."""
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    unix_socket_path = os.environ[
        "INSTANCE_UNIX_SOCKET"
    ]

    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_pass,
            database=db_name,
            query={"unix_socket": unix_socket_path},
        ),
    )
    return pool

def fetch_skin_lesion(lesion_id: str):
    try:
        engine = connect_unix_socket()
        with engine.connect() as conn:
            query = text("SELECT * FROM skin_lesions WHERE id = :id")
            return conn.execute(query, {"id": lesion_id}).fetchone()
    except Exception as e:
        print(f"Database error: {str(e)}")
        return None

def update_lesion_status(lesion_id: str, status: str, 
                        classification: str = None, 
                        processed_image_url: str = None):
    try:
        engine = connect_unix_socket()
        with engine.connect() as conn:
            query = text("""
                UPDATE skin_lesions 
                SET status = :status,
                    classification = :classification,
                    processedImageUrl = :processedImageUrl,
                    processedAt = NOW()
                WHERE id = :id
            """)
            conn.execute(query, {
                "id": lesion_id,
                "status": status,
                "classification": classification,
                "processedImageUrl": processed_image_url
            })
    except Exception as e:
        print(f"Database update error: {str(e)}")