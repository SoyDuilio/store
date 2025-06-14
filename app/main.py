# app/main.py

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from weasyprint import HTML
from datetime import datetime

# --- CONFIGURACIÓN DE LA APLICACIÓN ---
app = FastAPI(title="Generador de Ebooks de Belleza")

# Montar archivos estáticos (CSS, JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configurar plantillas Jinja2 en modo asíncrono
templates = Jinja2Templates(directory="app/templates", enable_async=True)


# --- BASE DE DATOS SIMULADA ---
def get_user_from_db(user_id: int):
    """Simula una consulta a la base de datos para obtener datos del usuario."""
    fake_users = {
        1: {"name": "Ana Lucía Torres"},
        2: {"name": "Carla Mendoza"},
        3: {"name": "Lectora VIP"}
    }
    return fake_users.get(user_id)


# --- ENDPOINTS DE LA API ---

@app.get("/ebook/view/{user_id}", response_class=HTMLResponse)
async def view_ebook(request: Request, user_id: int):
    """Muestra una versión web interactiva del Ebook."""
    user_data = get_user_from_db(user_id)
    if not user_data:
        return HTMLResponse("<h1>Usuario no encontrado</h1>", status_code=404)

    context = {
        "request": request,
        "reader_name": user_data["name"],
        "reader_id": user_id,  # Necesario para el botón de descarga en la plantilla
        "generation_date": datetime.now().strftime("%d de %B de %Y")
    }

    html_template = templates.get_template("ebook_template.html")
    content = await html_template.render_async(context)
    return HTMLResponse(content=content)


@app.get("/ebook/download/{user_id}")
async def generate_pdf_ebook(request: Request, user_id: int):
    """Genera un Ebook en PDF con diseño moderno usando WeasyPrint."""
    user_data = get_user_from_db(user_id)
    if not user_data:
        return HTMLResponse("<h1>Usuario no encontrado</h1>", status_code=404)

    context = {
        "request": request,
        "reader_name": user_data["name"],
        "reader_id": user_id,
        "generation_date": datetime.now().strftime("%d de %B de %Y")
    }

    # Renderiza la plantilla HTML a un string
    html_template = templates.get_template("ebook_template.html")
    html_string = await html_template.render_async(context)

    # Crea el objeto HTML de WeasyPrint
    # La URL base es crucial para que encuentre el archivo CSS enlazado en el HTML
    base_url = str(request.base_url)
    html_doc = HTML(string=html_string, base_url=base_url)

    # Renderiza el PDF en memoria
    pdf_bytes = html_doc.write_pdf()

    # Prepara y devuelve la respuesta
    pdf_filename = "Ebook-Domina-Tu-Territorio.pdf"
    return Response(
        content=pdf_bytes,
        media_type='application/pdf',
        headers={'Content-Disposition': f'attachment; filename="{pdf_filename}"'}
    )