# Archivo: app/routers/ebooks.py

from fastapi import APIRouter, Form, HTTPException
from ..schemas.documents import GenerationRequest, EbookState
import httpx  # Librería moderna para hacer llamadas HTTP, más potente que requests
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

router = APIRouter(
    prefix="/api/v1/ebooks",
    tags=["eBooks & Documents"]
)

# --- CONFIGURACIÓN DE LA API ---
API_KEY = os.getenv("MY_API_KEY")
# Usamos la IP directa para evitar cualquier problema de DNS
API_URL = "http://44.204.148.169:8080/v1/document-generator"

# --- ENDPOINT DE GENERACIÓN CON IA REAL ---
@router.post("/generate", response_model=EbookState)
async def generate_document(prompt: str = Form(...), blueprint: str = Form(...)):
    """
    Recibe un prompt y un blueprint, se conecta a la IA real
    y devuelve la estructura completa del EbookState en formato JSON.
    """
    if not API_KEY:
        raise HTTPException(status_code=500, detail="La clave de la API no está configurada en el servidor.")

    print(f"Iniciando llamada a la API real: Prompt='{prompt}', Blueprint='{blueprint}'")

    # Estructura de la petición a la API
    payload = {
        "prompt": prompt,
        "blueprint": blueprint,
        "output_schema": EbookState.model_json_schema() # Enviamos el esquema Pydantic para que la IA sepa qué formato devolver
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    print(f"Iniciando llamada a la API real: Prompt='{prompt}', Blueprint='{blueprint}'")

    # AÑADE ESTA LÍNEA DEBAJO
    print(f"Intentando conectar a: {API_URL}") 


    # Usamos httpx para hacer la llamada asíncrona
    async with httpx.AsyncClient(timeout=180.0) as client: # Timeout de 60 segundos
        try:
            response = await client.post(API_URL, json=payload, headers=headers)
            response.raise_for_status() # Lanza un error si la respuesta es 4xx o 5xx

            # La respuesta de la API debería ser directamente el JSON del EbookState
            ebook_state_data = response.json()
            
            # Devolvemos los datos, FastAPI los validará contra el response_model EbookState
            return ebook_state_data

        except httpx.HTTPStatusError as e:
            # Error en la respuesta de la API (ej: 401 Unauthorized, 500 Internal Server Error)
            print(f"Error en la respuesta de la API: {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"Error al comunicarse con el servicio de IA: {e.response.text}")
        except Exception as e:
            # Otros errores (timeout, problema de red, etc.)
            print(f"Error inesperado al llamar a la API: {e}")
            raise HTTPException(status_code=500, detail=f"Ocurrió un error inesperado en el servidor: {e}")