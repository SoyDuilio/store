from fastapi import FastAPI
from .routers import campaigns, proposals, ebooks, ebooks_openAI, views, auth, uploads # Y los otros
from .database import engine, Base
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .routers import views, auth, uploads
from fastapi import Request
from fastapi.responses import HTMLResponse, Response
# En app/main.py

# Crea las tablas en la BD (esto se puede quitar una vez que uses Alembic)
# Base.metadata.create_all(bind=engine) 

app = FastAPI()

# --- CONFIGURACIÓN DE LA APLICACIÓN ---
app = FastAPI(title="Generador de Ebooks de Belleza")

# Montar archivos estáticos (CSS, JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configurar plantillas Jinja2
templates = Jinja2Templates(directory="app/templates")

# Añadir middleware para la sesión (¡importante para el login!)
from starlette.middleware.sessions import SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key="una-clave-secreta-muy-larga-y-dificil")


# ✔ HOME DEL SITIO 👈
@app.get("/", response_class=HTMLResponse)
async def duilio_home(request: Request):
    """
    Sirve la home de Duilio.store
    """
    return templates.TemplateResponse("index.html", {"request": request})

# ✔ HOME DEL SITIO 👈
@app.get("/onboarding", response_class=HTMLResponse)
async def get_onboarding_page(request: Request):
    """
    Sirve la página principal de onboarding donde el usuario inicia la creación.
    """
    return templates.TemplateResponse("onboarding.html", {"request": request})

@app.get("/approval", response_class=HTMLResponse)
async def get_approval_page(request: Request):
    """
    Sirve la nueva página de "Aprobación" donde el usuario revisa
    la propuesta de la IA (índice y ángulos de venta).
    """
    return templates.TemplateResponse("approval.html", {"request": request})


@app.get("/campaign-dashboard", response_class=HTMLResponse)
async def get_campaign_dashboard_page(request: Request):
    """
    Sirve la página final donde se muestran los 3 documentos
    de la campaña generada.
    """
    return templates.TemplateResponse("campaign-dashboard.html", {"request": request})



@app.get("/editor", response_class=HTMLResponse)
async def editor( request: Request):
    return templates.TemplateResponse("editor_v2.html", {"request": request})

app.include_router(campaigns.router)
app.include_router(proposals.router)
app.include_router(ebooks.router)
app.include_router(views.router)
app.include_router(auth.router)
app.include_router(uploads.router)
app.include_router(ebooks_openAI.router)
# ... incluir otros routers ...


#CEJAS main.im version 1
@app.get("/cejas4", response_class=HTMLResponse)
async def cejas4( request: Request):
    return templates.TemplateResponse("cejas_main_1.html", {"request": request})

#CEJAS main.im version 2
@app.get("/cejas5", response_class=HTMLResponse)
async def cejas5( request: Request):
    return templates.TemplateResponse("cejas_main_2.html", {"request": request})