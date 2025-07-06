# --- IMPORTACIONES ESENCIALES ---
# FastAPI es el framework principal para crear la aplicación.
# Request se necesita para que las plantillas Jinja2 puedan renderizar correctamente.
# StaticFiles permite servir archivos como CSS, JS e imágenes desde una carpeta.
# Jinja2Templates es el motor para renderizar las plantillas HTML.
# HTMLResponse y FileResponse son tipos de respuesta para enviar HTML y archivos.
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse

# --- IMPORTACIONES OPCIONALES PERO ÚTILES ---
# El logging es muy útil para depurar, incluso en un sitio estático. Muestra errores en la consola.
import logging
# El datetime se usa aquí solo para simular datos en el dashboard. Se podría quitar si no lo usas.
from datetime import datetime

# --- IMPORTACIONES COMENTADAS (NO NECESARIAS PARA SITIO ESTÁTICO) ---
# CORS es para permitir peticiones desde otros dominios. Si tu frontend y backend están en el mismo
# dominio (como en este caso), no es estrictamente necesario. Lo dejo por si tienes un caso de uso específico.
from fastapi.middleware.cors import CORSMiddleware
# TrustedHost es una medida de seguridad. Es buena práctica, pero para desarrollo local simple, se puede omitir.
from fastapi.middleware.trustedhost import TrustedHostMiddleware
# 'os' no se está utilizando en el código, por lo que se puede eliminar.
# import os

# --- SECCIÓN DE BASE DE DATOS (NO NECESARIA) ---
# Todas estas importaciones están relacionadas con la base de datos, autenticación de usuarios,
# y rutas dinámicas (API). Para un sitio estático, no se necesitan en absoluto.
"""
from app.database import engine, Base
from app.security import get_current_user, get_current_user_optional, require_role
from app.routes import auth, contacts, events, notifications, territories
from app.models.models import User
"""

# --- RUTAS DINÁMICAS (NO NECESARIAS) ---
# Estas rutas (views, contacts_review) probablemente contenían lógica de negocio o
# interacciones con la base de datos. Para un sitio puramente estático, no las incluimos.
"""
from app.routes import views, contacts_review
"""

# --- CONFIGURACIÓN DE LOGGING (ÚTIL PARA DEPURACIÓN) ---
# Esto configura un sistema de registro de eventos. Es muy recomendable mantenerlo
# para poder ver errores o información relevante en la consola al ejecutar uvicorn.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- CREACIÓN DE TABLAS DE BD (NO NECESARIA) ---
# Esta sección intentaba crear las tablas en la base de datos al iniciar la app.
# Como no usamos base de datos, se elimina por completo.
"""
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Tablas de base de datos creadas/verificadas exitosamente")
except Exception as e:
    logger.error(f"Error creando tablas: {e}")
"""

# --- INICIALIZACIÓN DE LA APLICACIÓN FASTAPI ---
# Esta es la línea central que crea tu aplicación web. Es indispensable.
app = FastAPI(
    title="CRM Político (Demo Estático)",
    version="1.0.0",
    # Puedes desactivar la documentación autogenerada si no la necesitas
    docs_url=None,
    redoc_url=None
)

# --- MIDDLEWARES (OPCIONALES PARA SITIO ESTÁTICO) ---
# Un middleware es una función que se ejecuta antes de cada petición.

# TrustedHostMiddleware: Es una capa de seguridad que previene ataques de "Host header".
# Es buena práctica tenerlo, pero si solo trabajas en local, podrías comentarlo.
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.tu-dominio.com"] # Añade tu dominio si despliegas
)

# CORSMiddleware: Solo es necesario si una página web de OTRO dominio (ej. un frontend en React
# en localhost:3000) necesita hacer peticiones a este servidor (en localhost:8000).
# Si todo se sirve desde el mismo lugar, esto es innecesario.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:2222", "http://127.0.0.1:2222"], # Orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- SERVICE WORKER (PARA PROGRESSIVE WEB APPS - PWA) ---
# Si tu sitio usa un Service Worker para funcionar offline o para notificaciones push,
# esta ruta es necesaria para servir el archivo sw.js.
@app.get("/sw.js", response_class=FileResponse, include_in_schema=False)
async def serve_sw():
    # Asegúrate de que el archivo 'sw.js' exista en el directorio raíz de tu proyecto.
    return "sw.js"


# --- CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS Y PLANTILLAS (ESENCIAL) ---
# "Monta" el directorio 'static' en la ruta URL '/static'. Esto permite que el navegador
# acceda a tus archivos CSS, JavaScript, imágenes, etc.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configura Jinja2 para buscar plantillas HTML en el directorio 'templates'.
templates = Jinja2Templates(directory="templates")

# (Opcional pero útil) Esta función auxiliar permite usar `url_for('nombre_ruta')` dentro
# de las plantillas HTML para generar URLs dinámicamente, evitando hardcodearlas.
def url_for(name: str, **path_params):
    return app.url_path_for(name, **path_params)
templates.env.globals.update(url_for=url_for)


# --- RUTAS DINÁMICAS EXTERNAS (NO NECESARIAS) ---
# Como se mencionó antes, estas rutas probablemente contienen lógica de backend.
# Para un sitio estático, las comentamos y definimos las rutas directamente aquí.
"""
app.include_router(contacts_review.router)
app.include_router(views.router)
"""

# --- DEFINICIÓN DE RUTAS PARA PÁGINAS ESTÁTICAS (ESENCIAL) ---
# Cada una de estas funciones define una URL y le dice a FastAPI qué archivo HTML
# debe renderizar cuando un usuario visita esa URL.

@app.get("/", response_class=HTMLResponse, name="home")
async def home_page(request: Request):
    # Devuelve la plantilla 'home.html'. El 'request' es obligatorio para Jinja2.
    # El 'user: None' es un remanente de cuando había un sistema de login.
    return templates.TemplateResponse("home.html", {"request": request, "user": None})

@app.get("/login", response_class=HTMLResponse, name="login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse, name="dashboard")
async def dashboard_router(request: Request):
    # Aquí se simulan datos dinámicos. El servidor genera estos datos cada vez que
    # se pide la página, pero no vienen de una base de datos.
    data = {
        'stats': {'total_contacts': 394, 'new_contacts_month': 28, 'total_supporters': 93, 'support_percentage': 80, 'upcoming_events': 8, 'total_districts': 7},
        'recent_activities': [{'type': 'users', 'description': 'Grupo "Comerciantes Centro" actualizado', 'time_ago': 'hace 2 horas'}],
        'upcoming_events': [{'title': 'Reunión Vecinal Norte', 'location': 'Salón Comunal', 'date': datetime.now(), 'time': '19:00', 'confirmed_attendees': 50}]
    }
    return templates.TemplateResponse("dashboard_analytical.html", {"request": request, **data})

@app.get("/register-contact", response_class=HTMLResponse, name="register_contact")
async def register_contact_page(request: Request):
    return templates.TemplateResponse("register_contact.html", {"request": request, "user": None})

# --- MANEJADORES DE ERRORES (BUENA PRÁCTICA) ---
# Sirven páginas de error personalizadas en lugar de las genéricas del navegador.

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    # Cuando una página no se encuentra (error 404), muestra '404.html'.
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # Para cualquier otro error inesperado en el servidor (error 500).
    logger.error(f"Error 500 no manejado: {exc}")
    return templates.TemplateResponse("error.html", {
        "request": request,
        "error_message": "Ocurrió un error interno inesperado."
    }, status_code=500)


# --- RUTA DE TEST (OPCIONAL) ---
# Esta ruta es útil para verificar rápidamente si el servidor está funcionando.
# Devuelve un JSON simple. Puedes eliminarla si no la necesitas.
@app.get("/test")
async def test_route():
    return {"message": "La aplicación base sin base de datos funciona"}


# --- RUTAS DEL BLOG (PÁGINAS ESTÁTICAS ADICIONALES) ---
# NOTA: Has nombrado varias rutas como "home". Esto puede causar problemas con la función
# `url_for('home')`. Es mejor darles nombres únicos, como "alcaldea_home", "reeligete_home", etc.
@app.get("/alcaldea", response_class=HTMLResponse, name="alcaldea_home") # Nombre cambiado
async def home_alcaldes(request: Request):
    return templates.TemplateResponse("blog_alcaldes/landing_maestra.html", {"request": request})

@app.get("/reeligete", response_class=HTMLResponse, name="reeligete_page") # Nombre cambiado
async def reeligete(request: Request):
    return templates.TemplateResponse("blog_alcaldes/reeligete.html", {"request": request})

@app.get("/duilia1", response_class=HTMLResponse, name="duilia1_page") # Nombre cambiado
async def duilia1(request: Request):
    return templates.TemplateResponse("duilia_chatgpt.html", {"request": request})

@app.get("/duilia2", response_class=HTMLResponse, name="duilia2_page") # Nombre cambiado
async def duilia2(request: Request):
    return templates.TemplateResponse("duilia_claude.html", {"request": request})


# --- LISTADO DE RUTAS (HERRAMIENTA DE DESARROLLO) ---
# Este bloque de código se ejecuta UNA VEZ, cuando inicias el servidor.
# Su única función es imprimir en la consola una tabla con todas las rutas que has definido.
# Es muy útil para depurar, pero no afecta al funcionamiento del servidor en sí.
# Puedes comentarlo o eliminarlo sin problemas.
try:
    from tabulate import tabulate
    print("\n" + "="*80)
    print("                 RUTAS REGISTRADAS EN LA APLICACIÓN")
    print("="*80)

    routes_data = []
    for route in app.routes:
        if hasattr(route, "methods"):
            routes_data.append([route.path, ", ".join(route.methods), route.name])
        elif hasattr(route, "path"): # Para rutas montadas como /static
            routes_data.append([route.path, "MOUNTED", route.name])

    print(tabulate(routes_data, headers=["Path", "Methods", "Name"], tablefmt="fancy_grid"))
    print("="*80 + "\n")
except ImportError:
    print("\n[INFO] 'tabulate' no está instalado. Omitiendo la tabla de rutas.\n")


# --- EJECUCIÓN DEL SERVIDOR (NO RECOMENDADO AQUÍ) ---
# La forma estándar de ejecutar una aplicación uvicorn es desde la terminal:
# > uvicorn app.main:app --reload
# Dejar esta línea comentada es la práctica correcta. Actívala solo si quieres
# ejecutar el servidor corriendo este script directamente con `python app/main.py`.
