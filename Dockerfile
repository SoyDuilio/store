# Usa una imagen base de Python. 'slim' es más ligera.
# Asegúrate de que la versión de Python coincida con la tuya (ej. 3.12, 3.11, etc.)
FROM python:3.12-slim

# Instala las dependencias de sistema que WeasyPrint necesita
# Usamos apt-get, el gestor de paquetes de Debian/Ubuntu
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libgobject-2.0-0 \
    # Añadimos otras dependencias comunes de WeasyPrint para evitar futuros problemas
    libharfbuzz0b \
    libfontconfig1 \
    libffi-dev \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia tu archivo de requerimientos de Python y los instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de tu aplicación al contenedor
COPY . .

# Comando para iniciar tu aplicación.
# AJÚSTALO según tu archivo principal y el nombre de tu app de FastAPI/Flask.
# El comando usa la variable de entorno $PORT que Railway proporciona.
# Ejemplo para FastAPI: uvicorn [nombre_modulo]:[nombre_app]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "$PORT"]