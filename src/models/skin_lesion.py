from enum import Enum

class SkinLesionStatus(str, Enum):
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'