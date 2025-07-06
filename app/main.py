# app/main.py

from fastapi import FastAPI
# ----------------- CAMBIOS AQUÍ -----------------
# 1. Comentamos la importación de los routers que usan la base de datos.
#    Esto evita que se ejecute el código dentro de ellos al arrancar.
# from app.routers import campaigns, proposals, ebooks, ebooks_openAI, views, auth, uploads

# 2. Comentamos la importación de la base de datos.
#    Esta es la causa principal del error.
# from app.database import engine, Base
# ------------------------------------------------

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse, Response

# Base.metadata.create_all(bind=engine) # Esto ya estaba comentado, pero es correcto

app = FastAPI()

# --- CONFIGURACIÓN DE LA APLICACIÓN ---
# He quitado la re-declaración de `app = FastAPI(...)` que era redundante.
app.title = "Generador de Ebooks de Belleza"

# Montar archivos estáticos (CSS, JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configurar plantillas Jinja2
templates = Jinja2Templates(directory="app/templates")

# ----------------- CAMBIO OPCIONAL PERO RECOMENDADO -----------------
# 3. Comentamos el middleware de sesión, ya que se usa para el login (auth)
#    que hemos desactivado. Así la app es aún más ligera.
# from starlette.middleware.sessions import SessionMiddleware
# app.add_middleware(SessionMiddleware, secret_key="una-clave-secreta-muy-larga-y-dificil")
# ---------------------------------------------------------------------


# ======================================================================
# ESTAS RUTAS NO DEPENDEN DE LA BASE DE DATOS Y FUNCIONARÁN PERFECTAMENTE
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
async def cmr_politico_page(request: Request): # He cambiado el nombre de la función para que no se repita
    """
    Sirve la página del CMR Político.
    """
    return templates.TemplateResponse("elecciones_bilingue.html", {"request": request})

# ✔ Otras páginas estáticas 👈
# Estas también funcionarán sin problema.
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

# ----------------- CAMBIOS AQUÍ -----------------
# 4. Comentamos todos los `include_router`. Si no lo hacemos, la app fallará
#    porque las variables (campaigns, auth, etc.) no fueron importadas.
# app.include_router(campaigns.router)
# app.include_router(proposals.router)
# app.include_router(ebooks.router)
# app.include_router(views.router)
# app.include_router(auth.router)
# app.include_router(uploads.router)
# app.include_router(ebooks_openAI.router)
# ------------------------------------------------
@app.get("/duilia1", response_class=HTMLResponse, name="duilia1_page") # Nombre cambiado
async def duilia1(request: Request):
    return templates.TemplateResponse("duilia_chatgpt.html", {"request": request})

@app.get("/duilia2", response_class=HTMLResponse, name="duilia2_page") # Nombre cambiado
async def duilia2(request: Request):
    return templates.TemplateResponse("duilia_claude.html", {"request": request})


