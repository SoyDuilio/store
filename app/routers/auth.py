import os
from fastapi import APIRouter, Request, Depends
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Importaciones de tu proyecto
from app.database import get_db
from app.models import user as user_model

# --- Configuración ---
load_dotenv()
router = APIRouter(
    prefix="/auth", # Es buena práctica prefijar las rutas de autenticación
    tags=["Authentication"] # Para la documentación de FastAPI
)
oauth = OAuth()

oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)
# --- Fin Configuración ---


# --- Endpoints ---

# Este endpoint debe estar fuera del prefijo /auth
@router.get('/login/google', include_in_schema=False)
async def login_via_google(request: Request):
    # La URL a la que Google debe redirigir al usuario
    # El nombre 'auth_callback' debe coincidir con el nombre de la función de abajo
    redirect_uri = request.url_for('auth_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get('/callback', include_in_schema=False)
async def auth_callback(request: Request, db: Session = Depends(get_db)):
    print("\n--- [DEBUG] INICIANDO CALLBACK DE GOOGLE ---")
    try:
        token = await oauth.google.authorize_access_token(request)
        print(f"--- [DEBUG] TOKEN OBTENIDO: {token}")
    except Exception as e:
        # Si algo falla, lo veremos claramente en la consola.
        print(f"!!!!!!!!!!!!!!! ERROR EN authorize_access_token !!!!!!!!!!!!!!!") # << AÑADIDO
        print(f"DETALLE DEL ERROR: {e}") # << AÑADIDO
        # Manejar error si el usuario cancela
        return RedirectResponse(url='/')

    user_info = token.get('userinfo')
    if not user_info:
        # Si el token no tiene la info, lo sabremos.
        print("!!!!!!!!!!!!!!! ERROR: 'userinfo' no encontrado en el token !!!!!!!!!!!!!!!") # << AÑADIDO
        # Manejar error si no se pudo obtener la info del usuario
        return RedirectResponse(url='/')
    
    print(f"--- [DEBUG] USER_INFO OBTENIDO: {user_info}") # << AÑADIDO


    # =========== INICIO DE LA LÓGICA DE BASE DE DATOS (LA PARTE CLAVE) ===========

    # 1. Intentar buscar al usuario por su email en nuestra tabla 'users'
    db_user = db.query(user_model.User).filter(user_model.User.email == user_info['email']).first()

    if not db_user:
        # 2. Si el usuario NO existe, lo CREAMOS
        print(f"Usuario no encontrado. Creando nuevo usuario: {user_info['email']}")
        new_user = user_model.User(
            google_id=user_info['sub'],
            email=user_info['email'],
            full_name=user_info.get('name'),
            picture_url=user_info.get('picture')
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        db_user = new_user # Asignamos el nuevo usuario para la sesión
    else:
        # 3. Si el usuario YA existe, ACTUALIZAMOS sus datos por si cambiaron
        print(f"Usuario encontrado. Actualizando datos para: {user_info['email']}")
        db_user.full_name = user_info.get('name')
        db_user.picture_url = user_info.get('picture')
        # El google_id y el email no deberían cambiar, así que no los tocamos.
        db.commit()

    # =========== FIN DE LA LÓGICA DE BASE DE DATOS ===========

    # 4. Guardar información en la sesión para mantener al usuario logueado
    # Guardamos solo lo necesario para mostrar en la UI, no todo el objeto
    request.session['user'] = {
        'email': db_user.email,
        'name': db_user.full_name,
        'picture': db_user.picture_url
    }
    
    print("--- [DEBUG] Sesión establecida. Redirigiendo al dashboard... ---") # << AÑADIDO
    # 5. Redirigir al usuario a su panel de control
    return RedirectResponse(url='/dashboard')


@router.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')