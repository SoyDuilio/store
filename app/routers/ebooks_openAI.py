# Archivo: app/routers/ebooks_openAI.py

from fastapi import APIRouter, Form, HTTPException
from ..schemas.documents import EbookState
import openai
import os
import json

# --- CONFIGURACIÓN DEL CLIENTE DE OPENAI ---
# Carga la clave de la API desde las variables de entorno (tu archivo .env)
# ¡Asegúrate de que tu clave está en .env como OPENAI_API_KEY="sk-..."!
try:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except TypeError:
    raise RuntimeError("La variable de entorno OPENAI_API_KEY no está configurada. Por favor, añádela a tu archivo .env")

router = APIRouter(
    prefix="/api/v1/openai",  # Usaremos un prefijo distinto para no chocar con el local
    tags=["OpenAI Generation"]
)


def build_smart_prompt(title: str, blueprint: str) -> str:
    """
    Construye un prompt muy detallado para la IA, pidiéndole la estructura del ebook
    Y TAMBIÉN 3 ángulos de venta estratégicos.
    """
    prompt = f"""
    Eres "Quantum Scribe", un experto estratega de marketing de contenidos y autor de best-sellers.
    Tu tarea es crear la estructura inicial para un documento digital y proponer ángulos de venta.

    **REGLAS ESTRICTAS DE SALIDA:**
    1.  Tu respuesta DEBE ser un único objeto JSON válido, sin ningún texto antes o después.
    2.  El JSON DEBE validar con la siguiente estructura Pydantic:
        {{
            "id": "string (UUID v4)",
            "title": "string (El título principal y pulido del ebook)",
            "components": [ ... ],
            "sales_angles": [
                {{
                    "title": "string (Título del ángulo de venta 1)",
                    "description": "string (Descripción del ángulo 1)"
                }},
                {{
                    "title": "string (Título del ángulo de venta 2)",
                    "description": "string (Descripción del ángulo 2)"
                }},
                {{
                    "title": "string (Título del ángulo de venta 3)",
                    "description": "string (Descripción del ángulo 3)"
                }}
            ]
        }}
    3.  NO uses saltos de línea (\\n) dentro del contenido.
    4.  Crea al menos 3-4 componentes 'capitulo_texto'.
    5.  **Genera EXACTAMENTE 3 ángulos de venta únicos y estratégicos.**

    **DATOS DE ENTRADA:**
    - Título/Idea del Documento: "{title}"
    - Tipo de Documento (Blueprint): "{blueprint}"

    **TU TAREA:**
    1.  **Análisis y Borrador:** Analiza la idea, deduce el nicho, crea un título atractivo y genera la estructura de componentes del ebook como hiciste antes.
    2.  **Estrategia de Venta:** Después de crear el borrador, piensa como un marketer. Basado en la idea "{title}", genera 3 ángulos de venta distintos y persuasivos. Cada ángulo debe tener un título de gancho y una breve descripción de por qué es efectivo para el público objetivo.
    3.  **Ensambla el JSON Completo:** Construye el objeto JSON final incluyendo tanto los `components` del ebook como los `sales_angles`.

    Ahora, genera el JSON completo para el documento solicitado.
    """
    return prompt


@router.post("/generate", response_model=EbookState)
async def generate_document_with_openai(prompt: str = Form(...), blueprint: str = Form(...)):
    """
    Recibe un prompt y un blueprint, construye un prompt inteligente,
    lo envía a OpenAI y devuelve el EbookState generado por la IA.
    """
    print(f"Petición recibida para OpenAI: Prompt='{prompt}', Blueprint='{blueprint}'")
    
    intelligent_prompt = build_smart_prompt(prompt, blueprint)

    try:
        print("Enviando petición a la API de OpenAI...")
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",  # Este modelo es bueno para seguir instrucciones JSON
            response_format={"type": "json_object"}, # ¡Magia! Le pedimos que fuerce una salida JSON
            messages=[
                {"role": "system", "content": intelligent_prompt},
                {"role": "user", "content": f"Genera el documento JSON para la idea: '{prompt}'"}
            ]
        )
        print("Respuesta recibida de OpenAI.")
        
        # Extraemos el contenido JSON de la respuesta
        response_content = completion.choices[0].message.content
        
        # Convertimos la cadena JSON en un diccionario de Python
        generated_data = json.loads(response_content)
        
        # Validamos con Pydantic y devolvemos
        return EbookState(**generated_data)

    except openai.APIStatusError as e:
        print(f"ERROR de OpenAI: {e}")
        raise HTTPException(status_code=500, detail=f"Error en la API de OpenAI: {e.message}")
    except (json.JSONDecodeError, TypeError) as e:
        print(f"ERROR de parsing JSON: {e}")
        raise HTTPException(status_code=500, detail="La respuesta de la IA no fue un JSON válido.")
    except Exception as e:
        print(f"ERROR inesperado: {e}")
        raise HTTPException(status_code=500, detail="Ha ocurrido un error inesperado.")