# Archivo: app/routers/ebooks.py (Versión 2.0 - Con Muestra Realista)

from fastapi import APIRouter, Form, HTTPException
from ..schemas.documents import EbookState
import json
import os
import uuid # ¡Importante añadir uuid para generar nuevos IDs!

router = APIRouter(
    prefix="/api/v1/ebooks",
    tags=["eBooks & Documents (Local)"]
)

# --- FUNCIÓN GENERADORA LOCAL MEJORADA ---
def load_realistic_sample_document() -> dict:
    """
    Carga la estructura de EbookState desde un archivo JSON de muestra.
    Esto nos da un resultado 100% realista para desarrollo sin llamar a la API.
    """
    try:
        file_path = "app/data/sample_ebook.json"
        
        if not os.path.exists(file_path):
             raise FileNotFoundError
        
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            # --- MEJORA IMPORTANTE: Regenerar IDs ---
            # Para que cada documento de prueba sea único y no choque en la BD
            data['id'] = str(uuid.uuid4())
            for component in data.get('components', []):
                component['id'] = str(uuid.uuid4())
            
            return data
            
    except FileNotFoundError:
        print(f"ERROR: El archivo de muestra no se encontró en '{file_path}'")
        raise HTTPException(status_code=500, detail="Error del servidor: falta el archivo de muestra.")
    except json.JSONDecodeError:
        print(f"ERROR: El archivo de muestra en '{file_path}' no es un JSON válido.")
        raise HTTPException(status_code=500, detail="Error del servidor: el archivo de muestra está corrupto.")


# --- ENDPOINT DE GENERACIÓN QUE USA LA MUESTRA REALISTA ---
@router.post("/generate", response_model=EbookState)
async def generate_document_from_sample(prompt: str = Form(...), blueprint: str = Form(...)):
    """
    Ignora el prompt y el blueprint y devuelve directamente el contenido
    del archivo de muestra realista. Ideal para desarrollo y pruebas.
    """
    print(f"Sirviendo documento de muestra realista. Prompt='{prompt}' ignorado.")
    generated_data = load_realistic_sample_document()
    return generated_data