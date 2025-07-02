# Archivo: app/schemas/campaigns.py

from pydantic import BaseModel, Field
from typing import List
from app.schemas.documents import ChapterProposal, SalesAngleProposal # Importamos los modelos que ya teníamos

class CampaignGenerationRequest(BaseModel):
    """
    Define los datos que el frontend envía para generar una campaña completa.
    """
    refined_title: str
    language_profile: str
    final_index: List[ChapterProposal]
    selected_angle_ids: List[str]
    original_sales_angles: List[SalesAngleProposal]