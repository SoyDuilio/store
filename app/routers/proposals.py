# Archivo: app/routers/proposals.py

from fastapi import APIRouter, Form, HTTPException
from ..schemas.documents import StrategicProposal # Importamos nuestro nuevo esquema
import openai
import os
import json
from typing import Optional

# --- CONFIGURACIÓN DEL CLIENTE DE OPENAI (Como antes) ---
try:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except TypeError:
    raise RuntimeError("La variable de entorno OPENAI_API_KEY no está configurada.")

router = APIRouter(
    prefix="/api/v1/proposals", # Nuevo prefijo para este flujo
    tags=["Strategic Proposals"]
)

# --- EL NUEVO PROMPT INTELIGENTE ---
def build_proposal_prompt(title_idea: str, language_profile: str, context: Optional[str]) -> str:
    """
    Construye el prompt para la Fase 1: generar el índice, los ángulos de venta y los avatares.
    """

    # Construimos una sección de contexto solo si el usuario la proporcionó
    context_section = ""
    if context:
        context_section = f"""
    **CONTEXTO ADICIONAL PROPORCIONADO POR EL USUARIO:**
    ---
    {context}
    ---
    """

    prompt = f"""
    Eres "Quantum Strategist", un experto mundial en marketing de contenidos y estratega de lanzamientos.
    Tu tarea es analizar una idea de documento y devolver un plan estratégico completo.

    {context_section}

    **REGLAS CRÍTICAS DE SALIDA:**
    1.  Tu respuesta DEBE ser un único objeto JSON válido, sin texto antes o después.
    2.  El JSON DEBE validar con la siguiente estructura Pydantic:
        {{
            "refined_title": "string",
            "proposed_index": [ {{ "title": "string" }} ],
            "sales_angles": [
                {{
                    "id": "string (un UUID v4 simple, ej: 'angle-1')",
                    "title": "string",
                    "description": "string",
                    "avatar": {{
                        "profile_type": "string",
                        "age_range": "string"
                    }}
                }}
            ]
        }}
    3.  El idioma de TODO el contenido que generes debe ser: **{language_profile}**.
    4.  Genera un índice (`proposed_index`) con al menos 5-7 capítulos relevantes.
    5.  Genera EXACTAMENTE 5 ángulos de venta (`sales_angles`) distintos y persuasivos. Cada uno debe tener su propio avatar definido.

    **DATOS DE ENTRADA:**
    - Idea Inicial: "{title_idea}"
    - Idioma y Público Objetivo: "{language_profile}"

    **TU PROCESO MENTAL:**
    1.  **Refinar Título:** Toma la idea inicial y conviértela en un título principal atractivo y optimizado para el público {language_profile}.
    2.  **Estructurar Contenido:** Diseña una tabla de contenidos (índice) lógica y completa para un documento basado en esa idea.
    3.  **Idear Campaña:** Basado en la idea y el público, crea 5 ángulos de venta. Para cada ángulo, define un perfil de avatar claro y conciso (quiénes son, su rango de edad) que sería el más receptivo a ese ángulo. Asegúrate de que los ángulos sean variados (uno puede ser para principiantes, otro para expertos, uno enfocado en el miedo, otro en el beneficio, etc.).
    4.  **Ensamblar JSON:** Construye el objeto JSON final siguiendo estrictamente las reglas.

    Ahora, ejecuta tu proceso y genera el JSON del plan estratégico.
    """
    return prompt

# --- EL NUEVO ENDPOINT DE GENERACIÓN DE PROPUESTAS ---
@router.post("/generate", response_model=StrategicProposal)
async def generate_proposal(
    prompt: str = Form(..., alias="title_idea"), # Usamos alias para que coincida con nuestro HTML
    language: str = Form(..., alias="language_profile"),
    context: Optional[str] = Form(None) # Aceptamos un campo 'context' que puede ser opcional
):
    """
    Recibe la idea inicial y el perfil de idioma, y devuelve una propuesta estratégica completa.
    """
    # --- LÍNEA MODIFICADA ---
    print(f"Recibida solicitud: Idea='{prompt}', Idioma='{language}', Contexto='{context}'")
    
    # --- LÍNEA MODIFICADA ---
    intelligent_prompt = build_proposal_prompt(prompt, language, context)

    try:
        print("Enviando petición a OpenAI para la propuesta estratégica...")
        completion = client.chat.completions.create(
            model="gpt-4o-mini", # Usamos el modelo más reciente y rentable
            response_format={"type": "json_object"},
            timeout=180.0, # <-- AÑADE ESTA LÍNEA (180 segundos = 3 minutos)
            messages=[
                {"role": "system", "content": intelligent_prompt},
                {"role": "user", "content": f"Genera el plan para la idea: '{prompt}'"}
            ]
        )
        print("Respuesta de propuesta estratégica recibida de OpenAI.")
        
        response_content = completion.choices[0].message.content
        generated_data = json.loads(response_content)
        
        # Pydantic valida automáticamente la respuesta gracias a `response_model`
        return generated_data

    except openai.APIStatusError as e:
        print(f"ERROR de OpenAI: {e}")
        raise HTTPException(status_code=500, detail=f"Error en la API de OpenAI: {e.message}")
    except (json.JSONDecodeError, TypeError) as e:
        print(f"ERROR de parsing JSON: {e}")
        raise HTTPException(status_code=500, detail="La respuesta de la IA no fue un JSON válido.")
    except Exception as e:
        print(f"ERROR inesperado: {e}")
        raise HTTPException(status_code=500, detail="Ha ocurrido un error inesperado.")