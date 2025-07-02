# Archivo: app/schemas/documents.py (Versión para la Arquitectura de "Revista de Lujo")

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import uuid

# ===================================================================
# DEFINICIONES FUNDAMENTALES
# ===================================================================

class ComponentInstance(BaseModel):
    """
    Representa una instancia de un componente dentro de una página.
    Es la pieza de construcción más básica.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    # El "nombre de fábrica" del componente, ej: "feature_card_3_col"
    # Esto le dice al frontend qué plantilla HTML cargar.
    component_type: str 
    # Un diccionario flexible que contiene los datos para rellenar la plantilla.
    # Ej: {"title": "Mi Título", "items": ["A", "B", "C"]}
    data: Dict[str, Any]

class Page(BaseModel):
    """
    Representa una única página del documento, que es un contenedor de componentes.
    Corresponde a una hoja A4 en el PDF final.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    # El nombre de la plantilla de página, ej: "layout_1_columna", "layout_2_columnas_hero"
    # Le dice al frontend cómo organizar los componentes en la página.
    page_template_type: str
    components: List[ComponentInstance]

class EbookState(BaseModel):
    """
    El estado completo de UN solo documento/revista.
    Es el objeto principal con el que trabajará toda la aplicación.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str # El título general del documento
    source_angle_title: Optional[str] = Field(None, description="El ángulo de venta que originó este doc.")
    
    # LA ESTRUCTURA CLAVE: Una lista de objetos de Página.
    pages: List[Page]

# ===================================================================
# MODELOS PARA EL FLUJO INICIAL (Propuesta y Campaña)
# Estos pueden quedarse como estaban, ya que su lógica es anterior
# a la maquetación final.
# ===================================================================

class ChapterProposal(BaseModel):
    title: str

class AvatarProfile(BaseModel):
    profile_type: str
    age_range: str

class SalesAngleProposal(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    avatar: AvatarProfile

class StrategicProposal(BaseModel):
    refined_title: str
    proposed_index: List[ChapterProposal]
    sales_angles: List[SalesAngleProposal]