# Archivo: app/routers/campaigns.py (COMPLETO - BLINDADO CONTRA ENCODING)

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse # Importamos JSONResponse
from pydantic import BaseModel
from app.schemas.campaigns import CampaignGenerationRequest
from app.schemas.documents import EbookState
from typing import List
import openai
import os
import json
import random

# --- CONFIGURACIÓN ---
try:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except TypeError:
    raise RuntimeError("La variable de entorno OPENAI_API_KEY no está configurada.")

router = APIRouter(
    prefix="/api/v1/campaigns",
    tags=["Campaign Generation"]
)

# --- BIBLIOTECAS Y CATÁLOGOS ---
THEME_LIBRARY = {
    "elegante": { "description": "Clásico y sofisticado.", "page_template_type": "layout_elegant_v1"},
    "moderno": { "description": "Limpio y audaz.", "page_template_type": "layout_modern_v1"},
    "creativo": { "description": "Vibrante y visual.", "page_template_type": "layout_creative_v1"}
}
COMPONENT_CATALOG = """
- `cover_elegant_v1`: Portada. Data: `{"title": "string", "subtitle": "string"}`.
- `cover_modern_v1`: Portada. Data: `{"title": "string", "subtitle": "string"}`.
- `cover_creativo_v1`: Portada. Data: `{"title": "string", "subtitle": "string"}`.
- `chapter_title_v1`: Título de capítulo. Data: `{"title": "string"}`.
- `text_block_simple_v1`: Párrafo de texto simple. Data: `{"text": "string"}`.
- `article_split_v1`: Artículo con imagen a la izquierda y texto en columnas a la derecha. Data: `{"text": "string", "alt_text": "string"}`.
- `image_full_bleed_v1`: Imagen a ancho completo (usar con moderación). Data: `{"image_url": "string (opcional)", "caption": "string"}`.
"""

def build_high_quality_document_prompt(request_data: CampaignGenerationRequest, target_angle, target_theme) -> str:
    index_str = "\n".join([f"- {chap.title}" for chap in request_data.final_index])
    example_output = {
      "id": "doc-uuid-1", "title": "Título Adaptado", "source_angle_title": target_angle.title,
      "pages": [
        {"id": "page-uuid-a", "page_template_type": THEME_LIBRARY[target_theme]["page_template_type"], "components": [{"id": "comp-uuid-b", "component_type": "cover_modern_v1", "data": {"title": "Título Portada", "subtitle": "Subtítulo"}}]},
        {"id": "page-uuid-c", "page_template_type": THEME_LIBRARY[target_theme]["page_template_type"], "components": [{"id": "comp-uuid-d", "component_type": "chapter_title_v1", "data": {"title": "Capítulo 1"}}, {"id": "comp-uuid-e", "component_type": "text_block_simple_v1", "data": {"text": "Contenido extenso y detallado con múltiples párrafos..."}}]}
      ]
    }

    prompt = f"""
    Eres "Quantum Publisher", un escritor experto y director de arte. Tu misión es producir UN ÚNICO documento de CALIDAD EXCEPCIONALMENTE ALTA.

    **REGLA CRÍTICA NÚMERO 1: ESTRUCTURA DE SALIDA**
    Tu respuesta DEBE ser un único objeto JSON que represente un solo `EbookState`. DEBE seguir la estructura del ejemplo al pie de la letra. No inventes ni omitas claves.
    **ESTRUCTURA Y EJEMPLO DE SALIDA (DEBES IMITAR ESTO A LA PERFECCIÓN):**
    ```json
    {json.dumps(example_output, indent=2, ensure_ascii=False)}
    ```

    **REGLA CRÍTICA NÚMERO 2: COMPONENTES**
    Para `component_type`, DEBES usar los nombres de este catálogo. Para `image_full_bleed_v1`, genera una URL real de Unsplash.
    **Catálogo de Componentes:**
    {COMPONENT_CATALOG}
    
    **REGLA CRÍTICA NÚMERO 3: CALIDAD Y MAQUETACIÓN DE REVISTA**
    Esta es la regla más importante. **No seas breve.** Para cada capítulo del índice, crea una maquetación rica y variada:
    1.  Empieza siempre con un `chapter_title_v1`.
    2.  Desarrolla el tema principal usando el componente `article_split_v1`. Escribe un texto **extenso y detallado** para este componente.
    3.  Si necesitas añadir más texto, usa uno o dos `text_block_simple_v1` a continuación.
    4.  Tu objetivo es crear una página que se vea como una revista profesional. Profundiza en cada tema.

    **DATOS PARA EL DOCUMENTO:**
    - Título General: "{request_data.refined_title}"
    - Tema de Diseño: "{target_theme}"
    - Ángulo de Venta: "{target_angle.title}"
    - Avatar Objetivo: "{target_angle.avatar.profile_type} ({target_angle.avatar.age_range})"
    - Índice a Desarrollar COMPLETAMENTE Y EN PROFUNDIDAD:
    {index_str}

    Ahora, enfoca toda tu energía en crear un solo documento espectacular, rico en contenido, visualmente atractivo y genera el JSON correspondiente.
    """
    return prompt

@router.post("/generate") # Eliminamos el response_model para manejar la respuesta manualmente
async def generate_campaign(request: CampaignGenerationRequest):
    print(f"Recibida solicitud para generar campaña para el título: '{request.refined_title}'")
    first_angle = next((angle for angle in request.original_sales_angles if angle.id in request.selected_angle_ids), None)
    if not first_angle:
        raise HTTPException(status_code=400, detail="No se encontró el ángulo de venta seleccionado.")
    target_theme = random.choice(list(THEME_LIBRARY.keys()))
    print(f"--- Enfocando generación en 1 documento de alta calidad (Tema: {target_theme}, Ángulo: {first_angle.title}) ---")
    high_quality_prompt = build_high_quality_document_prompt(request, first_angle, target_theme)
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": high_quality_prompt},
                {"role": "user", "content": f"Genera el documento de alta calidad para: '{request.refined_title}'"}
            ]
        )
        print("Respuesta de alta calidad recibida de OpenAI.")
        response_content = completion.choices[0].message.content
        
        # Validamos el único documento recibido
        high_quality_doc = EbookState.parse_raw(response_content)
        
        # --- SIMULACIÓN PARA EL DASHBOARD ---
        final_documents = []
        all_selected_angles = [a for a in request.original_sales_angles if a.id in request.selected_angle_ids]
        
        for angle in all_selected_angles:
            doc_clone = high_quality_doc.copy(deep=True)
            doc_clone.title = f"{angle.title}: {high_quality_doc.title}"
            doc_clone.source_angle_title = angle.title
            final_documents.append(doc_clone.model_dump()) # Usamos model_dump para convertir a dict
            
        # ===================================================================
        #           ¡¡¡AQUÍ ESTÁ LA ACTUALIZACIÓN CLAVE!!!
        # ===================================================================
        # Devolvemos una JSONResponse explícita para asegurar el encoding correcto
        return JSONResponse(content=final_documents)

    except Exception as e:
        print(f"ERROR inesperado durante la generación de alta calidad: {e}")
        raise HTTPException(status_code=500, detail="Ha ocurrido un error inesperado durante la generación del documento.")