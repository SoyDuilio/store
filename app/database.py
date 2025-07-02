from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Construir la URL de la base de datos usando las variables de entorno
# Formato: "postgresql://<user>:<password>@<host>:<port>/<dbname>"
DATABASE_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# Crear el motor de SQLAlchemy, que gestiona las conexiones a la BD
engine = create_engine(DATABASE_URL)

# Crear una clase SessionLocal. Cada instancia de esta clase será una sesión de base de datos.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear una clase Base. Nuestros modelos de SQLAlchemy (User, Template, etc.) heredarán de esta clase.
Base = declarative_base()

# Función de dependencia para obtener una sesión de BD en los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()