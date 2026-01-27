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
from fastapi.responses import HTMLResponse, Response, RedirectResponse, FileResponse
import os
# Base.metadata.create_all(bind=engine) # Esto ya estaba comentado, pero es correcto

app = FastAPI()

# --- CONFIGURACIÓN DE LA APLICACIÓN ---
# He quitado la re-declaración de `app = FastAPI(...)` que era redundante.
app.title = "Generador de Ebooks de Belleza"

# Montar archivos estáticos (CSS, JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configurar plantillas Jinja2
templates = Jinja2Templates(directory="app/templates")

# ==================== FAVICON ====================
@app.get("/favicon.ico")
async def favicon():
    favicon_path = os.path.join("app", "static", "img", "favicon.ico")
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path, media_type="image/x-icon")
    return Response(status_code=204)  # No Content si no existe

# ==================== SERVICE WORKER ====================
@app.get("/service-worker.js")
async def serve_service_worker():
    # El service-worker está en app/static/js/ según tu captura
    sw_path = os.path.join("app", "static", "js", "service-worker.js")
    return FileResponse(
        sw_path,
        media_type="application/javascript",
        headers={
            "Service-Worker-Allowed": "/",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )
# ==================== PWA ====================


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
@app.get("/roger", response_class=HTMLResponse)
async def roger(request: Request): # He cambiado el nombre de la función para que no se repita
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


#@app.get("/ong", response_class=HTMLResponse)
#async def ong(request: Request):
#    return templates.TemplateResponse("ong.html", {"request": request})


@app.get("/saludiquitos", response_class=HTMLResponse)
async def saludiquitos(request: Request):
    return templates.TemplateResponse("salud_iquitos.html", {"request": request})


@app.get("/mockup1", response_class=HTMLResponse)
async def mockup1(request: Request):
    return templates.TemplateResponse("mockup1.html", {"request": request})

@app.get("/mockup2", response_class=HTMLResponse)
async def mockup2(request: Request):
    return templates.TemplateResponse("mockup2.html", {"request": request})

#PROYECTO: SAAS - CREDITOS 💲🤑
@app.get("/vendedor", response_class=HTMLResponse)
async def vendedor(request: Request):
    return templates.TemplateResponse("vendedor.html", {"request": request})

@app.get("/registro", response_class=HTMLResponse)
async def registro(request: Request):
    return templates.TemplateResponse("registro.html", {"request": request})

@app.get("/credito", response_class=HTMLResponse)
async def credito(request: Request):
    return templates.TemplateResponse("nuevo_credito.html", {"request": request})

@app.get("/pagos", response_class=HTMLResponse)
async def pagos(request: Request):
    return templates.TemplateResponse("pagos.html", {"request": request})

@app.get("/supervisor", response_class=HTMLResponse)
async def supervisor(request: Request):
    return templates.TemplateResponse("supervisor.html", {"request": request})

@app.get("/caja", response_class=HTMLResponse)
async def caja(request: Request):
    return templates.TemplateResponse("control_caja.html", {"request": request})

@app.get("/reportes", response_class=HTMLResponse)
async def reportes(request: Request):
    return templates.TemplateResponse("reportes.html", {"request": request})

@app.get("/configuracion", response_class=HTMLResponse)
async def configuracion(request: Request):
    return templates.TemplateResponse("configuracion.html", {"request": request})


@app.get("/vfp", response_class=HTMLResponse)
async def vfp(request: Request):
    return templates.TemplateResponse("vfp.html", {"request": request})

@app.get("/odbc", response_class=HTMLResponse)
async def odbc(request: Request):
    return templates.TemplateResponse("odbc.html", {"request": request})

@app.get("/api", response_class=HTMLResponse)
async def api(request: Request):
    return templates.TemplateResponse("api_rest.html", {"request": request})


@app.get("/guia", response_class=HTMLResponse)
async def guia(request: Request):
    return templates.TemplateResponse("guia2.html", {"request": request})


@app.get("/misaas", response_class=HTMLResponse)
async def misaas(request: Request):
    return templates.TemplateResponse("saas.html", {"request": request})

#PROPUESTA TÉCNICA PARA SERVIPLUS
@app.get("/serviplus", response_class=HTMLResponse)
async def serviplus(request: Request):
    return templates.TemplateResponse("index_serviplus.html", {"request": request})

#PROPUESTA TÉCNICA PARA SERVIPLUS
@app.get("/serviplus1", response_class=HTMLResponse)
async def serviplus1(request: Request):
    return templates.TemplateResponse("serviplus1.html", {"request": request})

#ACLARACIONES TÉCNIAS POR PLAN
@app.get("/serviplus2", response_class=HTMLResponse)
async def serviplus2(request: Request):
    return templates.TemplateResponse("serviplus2.html", {"request": request})

#COSTOS DE RAILWAY
@app.get("/serviplus3", response_class=HTMLResponse)
async def serviplus3(request: Request):
    return templates.TemplateResponse("serviplus3.html", {"request": request})


#SIGCO-WEB PLAN PARA WALTER
@app.get("/sigcoweb", response_class=HTMLResponse)
async def sigcoweb(request: Request):
    return templates.TemplateResponse("sigcoweb_plan2.html", {"request": request})

#DOCUMENTACION- REDIS y CELERY
@app.get("/celery", response_class=HTMLResponse)
async def celery(request: Request):
    return templates.TemplateResponse("redis_celery.html", {"request": request})


#IST-PEDRO A DEL AGUILA
@app.get("/instituto", response_class=HTMLResponse)
async def instituto(request: Request):
    return templates.TemplateResponse("instituto_pada.html", {"request": request})

#IST-PEDRO A DEL AGUILA -EXAMEN ADMISION
@app.get("/examen", response_class=HTMLResponse)
async def examen(request: Request):
    return templates.TemplateResponse("examen_admision.html", {"request": request})

#IST-PEDRO A DEL AGUILA -PROPUESTA
@app.get("/propuesta", response_class=HTMLResponse)
async def propuesta(request: Request):
    return templates.TemplateResponse("propuesta.html", {"request": request})


#ESTADO PERUANO - ANTI SOBORNO
@app.get("/anti", response_class=HTMLResponse)
async def anti(request: Request):
    return templates.TemplateResponse("anti_soborno.html", {"request": request})


#COLEGI DE CONTADORES PUBLICOS - LORETO
@app.get("/colegio", response_class=HTMLResponse)
async def colegio(request: Request):
    return templates.TemplateResponse("ccp_loreto.html", {"request": request})


#PASARELAS PAGO - SERVIPLUS
@app.get("/pasarelas", response_class=HTMLResponse)
async def pasarelas(request: Request):
    return templates.TemplateResponse("pasarelas_pago_peru.html", {"request": request})

#WEB-SOCKETS & REDIS
@app.get("/redis", response_class=HTMLResponse)
async def redis(request: Request):
    return templates.TemplateResponse("websockets_redis.html", {"request": request})


#CONDOMINIA - JULIETH
@app.get("/paso0", response_class=HTMLResponse)
async def paso0(request: Request):
    return templates.TemplateResponse("paso0.html", {"request": request})


#COLEGIO CONTADORES LORETO - JORGE
@app.get("/decanojorge", response_class=HTMLResponse)
async def decanojorge(request: Request):
    return templates.TemplateResponse("decanojorge.html", {"request": request})

#COLEGIO CONTADORES LORETO - JORGE
@app.get("/saascolegios", response_class=HTMLResponse)
async def saascolegios(request: Request):
    return templates.TemplateResponse("saascolegios.html", {"request": request})


#ADMISION - IST PEDRO A DEL AGUILA H.
@app.get("/videos", response_class=HTMLResponse)
async def videos(request: Request):
    return templates.TemplateResponse("videos_demo.html", {"request": request})


#SERVIPLUS - TERMINOS Y CONDICIONES POR DEFINIR
@app.get("/terminos", response_class=HTMLResponse)
async def terminos(request: Request):
    return templates.TemplateResponse("terminos_condiciones.html", {"request": request})

#COLEGIO CONTADORES LORETO - PROPUESTA A JORGE SANTANA
@app.get("/jorgedecano", response_class=HTMLResponse)
async def jorgedecano(request: Request):
    return templates.TemplateResponse("jorgedecano.html", {"request": request})


#NUEVO PORTAL COLEGIO CONTADORES LORETO - PROPUESTA A JORGE SANTANA
@app.get("/portal", response_class=HTMLResponse)
async def portal(request: Request):
    return templates.TemplateResponse("portal.html", {"request": request})


#NUEVO PORTAL COLEGIO CONTADORES LORETO - PROPUESTA A JORGE SANTANA
@app.get("/nuevoportal", response_class=HTMLResponse)
async def nuevoportal(request: Request):
    return templates.TemplateResponse("nuevoportal.html", {"request": request})

#FUNCIONALIDADES COLEGIO CONTADORES LORETO - PROPUESTA A JORGE SANTANA (26-12-2025)
@app.get("/funcionalidades", response_class=HTMLResponse)
async def funcionalidades(request: Request):
    return templates.TemplateResponse("funcionalidades.html", {"request": request})

#PROPUESTA/OFERTA A COLEGIO CONTADORES LORETO - PROPUESTA A JORGE SANTANA (07-01-2026)
@app.get("/ofertaccpl", response_class=HTMLResponse)
async def ofertaccpl(request: Request):
    return templates.TemplateResponse("ofertaccpl.html", {"request": request})

#MODELOS SITIOS WEB - COLEGIOS PROFESIONALES - PERÚ (20 enero 2026)
@app.get("/colegiospro", response_class=HTMLResponse)
async def colegiospro(request: Request):
    return templates.TemplateResponse("colegiospro.html", {"request": request})

@app.get("/catalogo", response_class=HTMLResponse)
async def catalogo(request: Request):
    return templates.TemplateResponse("catalogo.html", {"request": request})


#PROPUESTA PARA WALTER - MARCA BLANCA DE FACTURALO.PRO (24 enero 2026)
@app.get("/facturalo1", response_class=HTMLResponse)
async def facturalo1(request: Request):
    return templates.TemplateResponse("marca_blanca.html", {"request": request})

#LEVANTAMIENTO DE INFORMACIÓN - COLEGIO CONTADORES (SIRVE PARA TODO COLEGIO) (27-eNERO)
@app.get("/infocolegiospro", response_class=HTMLResponse)
async def infocolegiospro(request: Request):
    return templates.TemplateResponse("info_colegios.html", {"request": request})
