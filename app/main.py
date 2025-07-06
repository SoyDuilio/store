# app/main.py (Versión Corregida y Simplificada)

from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import os
import logging
from typing import Optional
from datetime import datetime

# Tus imports de la app (esto está bien)
from app.database import engine, Base
from app.security import get_current_user, get_current_user_optional, require_role
from app.routes import auth, contacts, events, notifications, territories
from app.models.models import User

from app.routes import views, contacts_review

# Configuración de Logging (esto está bien)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Crear tablas (esto está bien)
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Tablas de base de datos creadas/verificadas exitosamente")
except Exception as e:
    logger.error(f"Error creando tablas: {e}")

app = FastAPI(title="CRM Político", version="1.0.0")

# --- MIDDLEWARES (Ordenados y Simplificados) ---

# 1. TrustedHostMiddleware (Seguridad básica)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1"]
)

# 2. CORSMiddleware (Para comunicación entre dominios)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:2222", "http://127.0.0.1:2222"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- FIN DE MIDDLEWARES ---
# Eliminamos los @app.middleware("http") personalizados.
# La lógica de autenticación se manejará con Depends() en cada ruta, que es más explícito y menos propenso a errores.
# El manejo de errores se delega a los @app.exception_handler, que es la forma recomendada.

# --- SIRVIENDO EL SERVICE WORKER DESDE LA RAÍZ ---
@app.get("/sw.js", response_class=FileResponse)
async def serve_sw():
    return "sw.js"



# --- ARCHIVOS ESTÁTICOS Y TEMPLATES ---
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def url_for(name: str, **path_params):
    return app.url_path_for(name, **path_params)
templates.env.globals.update(url_for=url_for)

# --- RUTAS DE LA API ---
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
app.include_router(events.router, prefix="/events", tags=["events"])
app.include_router(notifications.router, prefix="/notifications", tags=["notifications"]) # <-- LÍNEA DESCOMENTADA
# app.include_router(territories.router, prefix="/territories", tags=["territories"])
app.include_router(contacts_review.router)
app.include_router(views.router)

# --- FUNCIONES DE DATOS (Mantenidas como estaban) ---
# ... (aquí van tus funciones get_dashboard_data, get_lider_grupal_dashboard_data, etc. Sin cambios) ...
async def get_dashboard_data():
    return {'stats': {'total_contacts': 394, 'new_contacts_month': 28, 'total_supporters': 93, 'support_percentage': 80, 'upcoming_events': 8, 'total_districts': 7}, 'recent_activities': [{'type': 'users', 'description': 'Grupo "Comerciantes Centro" actualizado', 'time_ago': 'hace 2 horas'}], 'upcoming_events': [{'title': 'Reunión Vecinal Norte', 'location': 'Salón Comunal', 'date': datetime.now(), 'time': '19:00', 'confirmed_attendees': 50}]}

async def get_lider_grupal_dashboard_data(user: User):
    return {"user": user, "total_contacts_in_group": 15, "latest_contacts": [{"name": "Juan Pérez", "time_ago": "hace 2 horas"}], "next_event": {"name": "Reunión Vecinal Norte", "date": "8 de Julio"}}

async def get_analytical_dashboard_data(user: User):
    data = await get_dashboard_data()
    return {"user": user, **data}

# --- RUTAS PRINCIPALES DE LA APLICACIÓN ---

@app.get("/", response_class=HTMLResponse, name="home")
async def home_page(request: Request, current_user: Optional[User] = Depends(get_current_user_optional)):
    return templates.TemplateResponse("home.html", {"request": request, "user": current_user})

@app.get("/login", response_class=HTMLResponse, name="login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse, name="dashboard")
async def dashboard_router(request: Request, current_user: User = Depends(get_current_user)):
    role = current_user.role
    analytical_roles = ["admin", "coordinador", "lider_distrital", "lider_provincial", "super_usuario", "candidato"]
    if role == "lider_grupal":
        data = await get_lider_grupal_dashboard_data(user=current_user)
        return templates.TemplateResponse("dashboard_lider_grupal.html", {"request": request, **data})
    elif role in analytical_roles:
        data = await get_analytical_dashboard_data(user=current_user)
        return templates.TemplateResponse("dashboard_analytical.html", {"request": request, **data})
    else:
        raise HTTPException(status_code=403, detail="Tu rol no tiene un dashboard asignado.")

# --- La protección se hace ahora DENTRO de cada ruta que la necesite ---
@app.get("/register-contact", response_class=HTMLResponse, name="register_contact")
async def register_contact_page(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse("register_contact.html", {"request": request, "user": user})


# --- MANEJO DE ERRORES GLOBALES (Recomendado) ---
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
    return {"message": "La aplicación base funciona"}



import uvicorn
from tabulate import tabulate

print("\n" + "="*80)
print("                 RUTAS REGISTRADAS EN LA APLICACIÓN")
print("="*80)

routes_data = []
for route in app.routes:
    # Para APIRoute normal
    if hasattr(route, "methods"):
        routes_data.append([route.path, ", ".join(route.methods), route.name])
    # Para Mounted applications (como StaticFiles)
    elif hasattr(route, "path"):
            routes_data.append([route.path, "MOUNTED", route.name])

print(tabulate(routes_data, headers=["Path", "Methods", "Name"], tablefmt="fancy_grid"))
print("="*80 + "\n")

# Esto te permite correr la app con `python app/main.py`
#uvicorn.run(app, host="0.0.0.0", port=8000)


# En app/main.py
@app.get("/notifications-dashboard", response_class=HTMLResponse, name="notifications_dashboard")
async def notifications_dashboard_page(request: Request, user: User = Depends(require_role("lider_grupal"))):
    # Aquí también puedes pasar datos si el formulario lo necesita (ej. lista de territorios)
    return templates.TemplateResponse("dashboard_notifications.html", {"request": request, "user": user})




# --- BLOG PARA ALCALDES ---

@app.get("/alcaldea", response_class=HTMLResponse, name="home")
async def home_alcaldes(request: Request):
    return templates.TemplateResponse("blog_alcaldes/landing_maestra.html", {"request": request})


@app.get("/reeligete", response_class=HTMLResponse, name="home")
async def reeligete(request: Request):
    return templates.TemplateResponse("blog_alcaldes/reeligete.html", {"request": request})

"""
#DUILIA
"""
@app.get("/duilia1", response_class=HTMLResponse, name="home")
async def duilia1(request: Request):
    return templates.TemplateResponse("duilia_chatgpt.html", {"request": request})


@app.get("/duilia2", response_class=HTMLResponse, name="home")
async def duilia2(request: Request):
    return templates.TemplateResponse("duilia_claude.html", {"request": request})