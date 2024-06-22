from typing import Optional

from pydantic import BaseModel


class PatientPrescriptionAdherence(BaseModel):
    adherence_rate: float
    reason: Optional[str] = None