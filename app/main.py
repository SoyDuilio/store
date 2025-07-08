# app/main.py

from fastapi import FastAPI
# ----------------- Importaciones originales comentadas (esto está correcto) -----------------
# from app.routers import campaigns, proposals, ebooks, ebooks_openAI, views, auth, uploads
# from app.database import engine, Base
# -----------------------------------------------------------------------------------------

# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, Response
from fastapi import Request

# --- CORRECCIÓN CLAVE ---
# Importamos desde el nuevo archivo de configuración
from .config import templates 
from . import demo_router


app = FastAPI()
app.title = "Duilio.store y Demo LICO System"
app.include_router(demo_router.router)

# Montar archivos estáticos (esto no cambia)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Incluimos el router de la demo
app.include_router(demo_router.router)


# ======================================================================
#             INICIO DE LA INTEGRACIÓN DE LA DEMO
# ======================================================================

# 1. Importa el router de la demo que contiene toda su lógica.
from app import demo_router

# ======================================================================
#             FIN DE LA INTEGRACIÓN DE LA DEMO
# ======================================================================

# Base.metadata.create_all(bind=engine) # Correctamente comentado

app = FastAPI()

# --- CONFIGURACIÓN DE LA APLICACIÓN ---
app.title = "Duilio.store y Demo LICO System"

# Montar archivos estáticos (CSS, JS) - Sirve para ambos proyectos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configurar plantillas Jinja2 - Sirve para ambos proyectos
templates = Jinja2Templates(directory="app/templates")

# ======================================================================
#             SECCIÓN PARA ACTIVAR LAS RUTAS DE LA DEMO
# ======================================================================

app.include_router(demo_router.router)

# Middleware de sesión original comentado (esto está correcto)
# from starlette.middleware.sessions import SessionMiddleware
# app.add_middleware(SessionMiddleware, secret_key="una-clave-secreta-muy-larga-y-dificil")

# ======================================================================
#             SECCIÓN PARA ACTIVAR LAS RUTAS DE LA DEMO
# ======================================================================

# 2. Incluye el router de la demo en la aplicación principal.
#    Esto hace que todas las rutas como /demo/login, /demo/gastos, etc., funcionen.
app.include_router(demo_router.router)

# ======================================================================
#             FIN DE LA SECCIÓN DE RUTAS DE LA DEMO
# ======================================================================


# ======================================================================
#      RUTAS ORIGINALES DE DUILIO.STORE (PERMANECEN INTACTAS)
# ======================================================================

# ✔ HOME DEL SITIO 👈
@app.get("/", response_class=HTMLResponse)
async def duilio_home(request: Request):
    """
    Sirve la home de Duilio.store
    """
    return templates.TemplateResponse("index.html", {"request": request})


# ✔ CMR POLITICO 👈
@app.get("/cmrpolitico", response_class=HTMLResponse)
async def cmr_politico_page(request: Request):
    """
    Sirve la página del CMR Político.
    """
    return templates.TemplateResponse("elecciones_bilingue.html", {"request": request})

# ✔ Otras páginas estáticas 👈
# (Las demás rutas de tu sitio estático permanecen aquí, sin cambios)
@app.get("/onboarding", response_class=HTMLResponse)
async def get_onboarding_page(request: Request):
    return templates.TemplateResponse("onboarding.html", {"request": request})

@app.get("/approval", response_class=HTMLResponse)
async def get_approval_page(request: Request):
    return templates.TemplateResponse("approval.html", {"request": request})

@app.get("/campaign-dashboard", response_class=HTMLResponse)
async def get_campaign_dashboard_page(request: Request):
    return templates.TemplateResponse("campaign-dashboard.html", {"request": request})

@app.get("/editor", response_class=HTMLResponse)
async def editor( request: Request):
    return templates.TemplateResponse("editor_v2.html", {"request": request})

@app.get("/cejas4", response_class=HTMLResponse)
async def cejas4( request: Request):
    return templates.TemplateResponse("cejas_main_1.html", {"request": request})

@app.get("/cejas5", response_class=HTMLResponse)
async def cejas5( request: Request):
    return templates.TemplateResponse("cejas_main_2.html", {"request": request})

# Routers originales comentados (esto está correcto)
# app.include_router(campaigns.router)
# ... etc ...

@app.get("/duilia1", response_class=HTMLResponse, name="duilia1_page")
async def duilia1(request: Request):
    return templates.TemplateResponse("duilia_chatgpt.html", {"request": request})

@app.get("/duilia2", response_class=HTMLResponse, name="duilia2_page")
async def duilia2(request: Request):
    return templates.TemplateResponse("duilia_claude.html", {"request": request})

@app.get("/duilia3", response_class=HTMLResponse, name="duilia3_page") # Nombre corregido
async def duilia3(request: Request):
    return templates.TemplateResponse("duilia_explica.html", {"request": request})
