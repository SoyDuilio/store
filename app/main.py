# app/main.py (Versión sin Base de Datos)

from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import os
import logging
from datetime import datetime

# Configuración de Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- NO USAR BASE DE DATOS ---
# from app.database import engine, Base
# from app.security import get_current_user, get_current_user_optional, require_role
# from app.routes import auth, contacts, events, notifications, territories
# from app.models.models import User

from app.routes import views, contacts_review

# Crear tablas (comentado)
# try:
#     Base.metadata.create_all(bind=engine)
#     logger.info("Tablas de base de datos creadas/verificadas exitosamente")
# except Exception as e:
#     logger.error(f"Error creando tablas: {e}")

app = FastAPI(title="CRM Político (Demo Estático)", version="1.0.0")

# --- MIDDLEWARES ---
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:2222", "http://127.0.0.1:2222"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SERVICE WORKER ---
@app.get("/sw.js", response_class=FileResponse)
async def serve_sw():
    return "sw.js"

# --- ARCHIVOS ESTÁTICOS Y TEMPLATES ---
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def url_for(name: str, **path_params):
    return app.url_path_for(name, **path_params)
templates.env.globals.update(url_for=url_for)

# --- RUTAS ACTIVAS (SOLO LAS ESTÁTICAS) ---
app.include_router(contacts_review.router)
app.include_router(views.router)

@app.get("/", response_class=HTMLResponse, name="home")
async def home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "user": None})

@app.get("/login", response_class=HTMLResponse, name="login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse, name="dashboard")
async def dashboard_router(request: Request):
    # Simulación de datos estáticos
    data = {
        'stats': {'total_contacts': 394, 'new_contacts_month': 28, 'total_supporters': 93, 'support_percentage': 80, 'upcoming_events': 8, 'total_districts': 7},
        'recent_activities': [{'type': 'users', 'description': 'Grupo "Comerciantes Centro" actualizado', 'time_ago': 'hace 2 horas'}],
        'upcoming_events': [{'title': 'Reunión Vecinal Norte', 'location': 'Salón Comunal', 'date': datetime.now(), 'time': '19:00', 'confirmed_attendees': 50}]
    }
    return templates.TemplateResponse("dashboard_analytical.html", {"request": request, **data})

@app.get("/register-contact", response_class=HTMLResponse, name="register_contact")
async def register_contact_page(request: Request):
    return templates.TemplateResponse("register_contact.html", {"request": request, "user": None})

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error 500 no manejado: {exc}")
    return templates.TemplateResponse("error.html", {
        "request": request,
        "error_message": "Ocurrió un error interno inesperado."
    }, status_code=500)

@app.get("/test")
async def test_route():
    return {"message": "La aplicación base sin base de datos funciona"}

# --- RUTAS BLOG ---
@app.get("/alcaldea", response_class=HTMLResponse, name="home")
async def home_alcaldes(request: Request):
    return templates.TemplateResponse("blog_alcaldes/landing_maestra.html", {"request": request})

@app.get("/reeligete", response_class=HTMLResponse, name="home")
async def reeligete(request: Request):
    return templates.TemplateResponse("blog_alcaldes/reeligete.html", {"request": request})

@app.get("/duilia1", response_class=HTMLResponse, name="home")
async def duilia1(request: Request):
    return templates.TemplateResponse("duilia_chatgpt.html", {"request": request})

@app.get("/duilia2", response_class=HTMLResponse, name="home")
async def duilia2(request: Request):
    return templates.TemplateResponse("duilia_claude.html", {"request": request})

# --- LISTADO DE RUTAS ---
from tabulate import tabulate
print("\n" + "="*80)
print("                 RUTAS REGISTRADAS EN LA APLICACIÓN")
print("="*80)

routes_data = []
for route in app.routes:
    if hasattr(route, "methods"):
        routes_data.append([route.path, ", ".join(route.methods), route.name])
    elif hasattr(route, "path"):
        routes_data.append([route.path, "MOUNTED", route.name])

print(tabulate(routes_data, headers=["Path", "Methods", "Name"], tablefmt="fancy_grid"))
print("="*80 + "\n")

# uvicorn.run(app, host="0.0.0.0", port=8000)  # ← Activar manualmente si se desea ejecutar
