from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from .mock_data import PERSONAL_MOCK, MOVIMIENTOS_PLANILLA_MOCK, GASTOS_MOCK

router = APIRouter(prefix="/demo", tags=["Demo"])
templates = Jinja2Templates(directory="templates")

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("/demo/login.html", {"request": request})

@router.post("/login")
async def handle_login(request: Request):
    form = await request.form()
    # Simulación de login: clave "1234" para el gerente
    if form.get("username") == "gerente" and form.get("password") == "1234":
        return RedirectResponse(url="/demo/dashboard", status_code=303)
    return RedirectResponse(url="/demo/login?error=1", status_code=303)

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("demo/dashboard.html", {"request": request})

@router.get("/gastos", response_class=HTMLResponse)
async def gastos_view(request: Request):
    return templates.TemplateResponse("demo/gastos.html", {"request": request, "gastos": GASTOS_MOCK})

@router.get("/planillas", response_class=HTMLResponse)
async def planillas_view(request: Request):
    return templates.TemplateResponse("demo/planillas.html", {"request": request, "personal": PERSONAL_MOCK})

@router.get("/personal/{personal_id}/liquidacion", response_class=HTMLResponse)
async def calcular_liquidacion(request: Request, personal_id: int):
    # Lógica de la liquidación (la "magia" de la demo)
    empleado = next((p for p in PERSONAL_MOCK if p["id"] == personal_id), None)
    if not empleado:
        return HTMLResponse("Empleado no encontrado", status_code=404)

    movimientos = MOVIMIENTOS_PLANILLA_MOCK.get(personal_id, [])
    
    sueldo = empleado["sueldo_base"]
    total_descuentos = sum(m["monto"] for m in movimientos if "DESCUENTO" in m["tipo"])
    total_adelantos = sum(m["monto"] for m in movimientos if "ADELANTO" in m["tipo"])
    total_bonos = sum(m["monto"] for m in movimientos if "BONO" in m["tipo"])
    
    monto_a_pagar = sueldo - total_descuentos - total_adelantos + total_bonos

    return templates.TemplateResponse("demo/liquidacion.html", {
        "request": request,
        "empleado": empleado,
        "movimientos": movimientos,
        "total_descuentos": total_descuentos,
        "total_adelantos": total_adelantos,
        "total_bonos": total_bonos,
        "monto_a_pagar": monto_a_pagar
    })

# Simulación del POS para mostrar el botón de escaneo
@router.get("/pos", response_class=HTMLResponse)
async def pos_view(request: Request):
    return templates.TemplateResponse("demo/pos_demo.html", {"request": request})


# --- FINANZAS: Pantalla para añadir un nuevo gasto ---
@router.get("/gastos/nuevo", response_class=HTMLResponse)
async def nuevo_gasto_form(request: Request):
    # En la vida real, los tipos de gasto y responsables vendrían de la DB
    tipos_gasto = ["Servicios", "Movilidad", "Compras", "Contador", "Sueldos"]
    responsables = ["Gerente", "Ana Paredes", "Luis Torres"]
    return templates.TemplateResponse("demo/form_gasto.html", {
        "request": request,
        "tipos_gasto": tipos_gasto,
        "responsables": responsables
    })

# --- PLANILLAS: Detalle del trabajador con foto ---
@router.get("/personal/{personal_id}", response_class=HTMLResponse)
async def detalle_personal(request: Request, personal_id: int):
    # Usamos los datos del mock_data.py
    empleado = next((p for p in PERSONAL_MOCK if p["id"] == personal_id), None)
    movimientos = MOVIMIENTOS_PLANILLA_MOCK.get(personal_id, [])
    
    # Añadimos una URL de foto falsa
    if empleado:
        empleado["foto_url"] = f"https://i.pravatar.cc/150?u={empleado['nombre_completo']}"
    
    return templates.TemplateResponse("demo/detalle_personal.html", {
        "request": request,
        "empleado": empleado,
        "movimientos": movimientos
    })

# --- REPORTES: Pantalla de demo con gráficos falsos ---
@router.get("/reportes/ventas", response_class=HTMLResponse)
async def reportes_ventas(request: Request):
    # Los datos para los gráficos se generarían aquí
    # Para la demo, los ponemos directamente en el HTML/JS
    return templates.TemplateResponse("demo/reporte_ventas.html", {"request": request})