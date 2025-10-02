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
from fastapi.responses import HTMLResponse, Response, RedirectResponse

# Base.metadata.create_all(bind=engine) # Esto ya estaba comentado, pero es correcto

app = FastAPI()

# --- CONFIGURACIÓN DE LA APLICACIÓN ---
# He quitado la re-declaración de `app = FastAPI(...)` que era redundante.
app.title = "Generador de Ebooks de Belleza"

# Montar archivos estáticos (CSS, JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configurar plantillas Jinja2
templates = Jinja2Templates(directory="app/templates")

# ======================================================================
#             2. DATOS SIMULADOS (MOCK DATA)
# ======================================================================
# Movemos los datos falsos aquí para que todas las rutas los puedan ver

PERSONAL_MOCK = [
    {
        "id": 1, 
        "nombre_completo": "Ana Paredes Rojas", 
        "cargo": "Cajera Principal / Supervisora de Turno", 
        "sueldo_base": 1350.00,
        "frecuencia_pago": "QUINCENAL"
    },
    {
        "id": 2, 
        "nombre_completo": "Luis Torres Vega", 
        "cargo": "Almacenero / Reponedor", 
        "sueldo_base": 1100.00,
        "frecuencia_pago": "MENSUAL"
    },
    {
        "id": 3, 
        "nombre_completo": "Carlos Mendoza Solis", 
        "cargo": "Cajero / Atención al Cliente", 
        "sueldo_base": 1050.00,
        "frecuencia_pago": "MENSUAL"
    },
    {
        "id": 4, 
        "nombre_completo": "Sofía Castro Luna", 
        "cargo": "Personal de Reparto (Delivery)", 
        "sueldo_base": 950.00,
        "frecuencia_pago": "SEMANAL"
    },
]
MOVIMIENTOS_PLANILLA_MOCK = {
    # Movimientos de Ana Paredes (ID 1)
    1: [
        {"tipo": "ADELANTO_EFECTIVO", "monto": 150.00, "descripcion": "Adelanto del 5 de mes para gastos personales"},
        {"tipo": "DESCUENTO_PRODUCTO", "monto": 28.00, "descripcion": "1x Vino Intipalka Malbec"},
        {"tipo": "BONO_DESEMPENO", "monto": 75.00, "descripcion": "Bono por superar meta de ventas quincenal"},
        {"tipo": "DESCUENTO_TARDANZA", "monto": 15.00, "descripcion": "Acumulado de 3 tardanzas en la quincena"},
    ],
    # Movimientos de Luis Torres (ID 2)
    2: [
        {"tipo": "ADELANTO_EFECTIVO", "monto": 50.00, "descripcion": "Adelanto para movilidad"},
        {"tipo": "DESCUENTO_PRODUCTO", "monto": 7.50, "descripcion": "1x Cerveza Cusqueña Trigo"},
        {"tipo": "BONO_FERIADO", "monto": 50.00, "descripcion": "Pago por trabajar feriado (Día del Trabajo)"},
    ],
    # Movimientos de Carlos Mendoza (ID 3)
    3: [
        {"tipo": "DESCUENTO_FALTA", "monto": 35.00, "descripcion": "Descuento por falta injustificada el 12/05"},
        {"tipo": "ADELANTO_EFECTIVO", "monto": 200.00, "descripcion": "Adelanto de sueldo"},
    ],
    # Movimientos de Sofía Castro (ID 4)
    4: [
        {"tipo": "BONO_DESEMPENO", "monto": 25.00, "descripcion": "Bono por entregas rápidas y sin quejas"},
    ]
}

GASTOS_MOCK = [
    {
        "id": 1, 
        "fecha": "2024-05-20", 
        "monto": 50.00, 
        "tipo": "Servicios", 
        "descripcion": "Pago de Internet del local (Mes de Mayo)", 
        "responsable": "Ana Paredes", 
        "autorizado_por": "Gerente"
    },
    {
        "id": 2, 
        "fecha": "2024-05-19", 
        "monto": 25.00, 
        "tipo": "Movilidad", 
        "descripcion": "Taxi para llevar documentos a la contadora", 
        "responsable": "Luis Torres", 
        "autorizado_por": "Gerente"
    },
    {
        "id": 3, 
        "fecha": "2024-05-18", 
        "monto": 250.00, 
        "tipo": "Compras", 
        "descripcion": "Compra de bolsas, six-packs de cartón y material de limpieza", 
        "responsable": "Ana Paredes", 
        "autorizado_por": "Gerente"
    },
    {
        "id": 4, 
        "fecha": "2024-05-15", 
        "monto": 150.00, 
        "tipo": "Contador", 
        "descripcion": "Pago honorarios contadora Sra. Elvira", 
        "responsable": "Gerente", 
        "autorizado_por": "Gerente"
    },
    {
        "id": 5, 
        "fecha": "2024-05-10", 
        "monto": 80.00, 
        "tipo": "Mantenimiento", 
        "descripcion": "Reparación de luz de letrero exterior", 
        "responsable": "Gerente", 
        "autorizado_por": "Gerente"
    },
    {
        "id": 6, 
        "fecha": "2024-05-02", 
        "monto": 120.00, 
        "tipo": "Servicios", 
        "descripcion": "Pago de servicio de agua y luz del local", 
        "responsable": "Ana Paredes", 
        "autorizado_por": "Gerente"
    }
]


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


# ✔ DUILIA - 2° CONTROL DE LECTURA CON CITAS👈
@app.get("/control2citas", response_class=HTMLResponse)
async def control2citas(request: Request): # He cambiado el nombre de la función para que no se repita
    """
    2° Control de Lectura - Maestría Duilia
    """
    return templates.TemplateResponse("control2-citas.html", {"request": request})

# ✔ DUILIA - 2° CONTROL DE LECTURA 👈
@app.get("/control2", response_class=HTMLResponse)
async def control2(request: Request): # He cambiado el nombre de la función para que no se repita
    """
    2° Control de Lectura - Maestría Duilia
    """
    return templates.TemplateResponse("control2.html", {"request": request})


# ✔ AVANCE - TIPS VENTAS -  NIEVES-CARLOS 👈
@app.get("/avance", response_class=HTMLResponse)
async def avance(request: Request): # He cambiado el nombre de la función para que no se repita
    """
    Ideas para vender más
    """
    return templates.TemplateResponse("avance.html", {"request": request})


# ✔ PROPUESTA NIEVES-CARLOS 👈
@app.get("/planes", response_class=HTMLResponse)
async def planes(request: Request): # He cambiado el nombre de la función para que no se repita
    """
    Propuesta Ventas
    """
    return templates.TemplateResponse("planes.html", {"request": request})

# ✔ SERVIDOR NIEVES-CARLOS 👈
@app.get("/servidor", response_class=HTMLResponse)
async def servidor(request: Request): # He cambiado el nombre de la función para que no se repita
    """
    Servidor, mínimo necesario, para servidor local
    """
    return templates.TemplateResponse("servidor.html", {"request": request})


# ✔ IMAGENES - JUAN NEYRA 🌦🔥
@app.get("/juan-cni", response_class=HTMLResponse)
async def juancni(request: Request): # He cambiado el nombre de la función para que no se repita
    """
    Servidor, mínimo necesario, para servidor local
    """
    return templates.TemplateResponse("juan_cni.html", {"request": request})



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

@app.get("/duilia3", response_class=HTMLResponse, name="duilia2_page") # Nombre cambiado
async def duilia3(request: Request):
    return templates.TemplateResponse("duilia_explica.html", {"request": request})

#DEMO LICO            DEMO LICO                DEMO LICO
@app.get("/demo/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("demo/login.html", {"request": request})

@app.post("/demo/login")
async def handle_login(request: Request):
    form = await request.form()
    # Simulación de login: clave "1234" para el gerente
    if form.get("username") == "gerente" and form.get("password") == "1234":
        # ESTA ES LA FORMA CORRECTA Y DEBE FUNCIONAR
        return RedirectResponse(url="/demo/dashboard", status_code=303)
    
    return RedirectResponse(url="/demo/login?error=1", status_code=303)

@app.get("/demo/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("demo/dashboard.html", {"request": request})

@app.get("/demo/gastos", response_class=HTMLResponse)
async def gastos_view(request: Request):
    return templates.TemplateResponse("demo/gastos.html", {"request": request, "gastos": GASTOS_MOCK})

@app.get("/demo/planillas", response_class=HTMLResponse)
async def planillas_view(request: Request):
    return templates.TemplateResponse("demo/planillas.html", {"request": request, "personal": PERSONAL_MOCK})

@app.get("/demo/personal/{personal_id}/liquidacion", response_class=HTMLResponse)
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
@app.get("/demo/pos", response_class=HTMLResponse)
async def pos_view(request: Request):
    return templates.TemplateResponse("demo/pos_demo.html", {"request": request})


# --- FINANZAS: Pantalla para añadir un nuevo gasto ---
@app.get("/demo/gastos/nuevo", response_class=HTMLResponse)
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
@app.get("/demo/personal/{personal_id}", response_class=HTMLResponse)
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
@app.get("/demo/reportes/ventas", response_class=HTMLResponse)
async def reportes_ventas(request: Request):
    # Los datos para los gráficos se generarían aquí
    # Para la demo, los ponemos directamente en el HTML/JS
    return templates.TemplateResponse("demo/reporte_ventas.html", {"request": request})


@app.get("/saas", response_class=HTMLResponse)
async def saas(request: Request):
    return templates.TemplateResponse("saas.html", {"request": request})


@app.get("/walter", response_class=HTMLResponse)
async def walter(request: Request):
    return templates.TemplateResponse("walter_saas.html", {"request": request})


@app.get("/ong", response_class=HTMLResponse)
async def ong(request: Request):
    return templates.TemplateResponse("ong.html", {"request": request})

