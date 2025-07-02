from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# ... tu endpoint para la ruta "/" ...
@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Si el usuario ya está logueado, lo mandamos al dashboard
    if "user" in request.session:
        return RedirectResponse(url="/dashboard")
    return templates.TemplateResponse("home.html", {"request": request})


# --- AÑADE ESTE NUEVO ENDPOINT ---
@router.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    user = request.session.get('user')
    # Si el usuario no está en la sesión, lo redirigimos a la página de inicio para que haga login
    if not user:
        return RedirectResponse(url="/")
    
    # Pasamos la información del usuario a la plantilla
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})