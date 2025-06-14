# Usa una imagen base de Python específica (Debian 12 Bookworm)
FROM python:3.12-slim-bookworm

# Variables de entorno recomendadas
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala las dependencias de sistema CORRECTAS para WeasyPrint
# NOTA: Cambiamos libgobject-2.0-0 por libgobject-2.0-dev y añadimos pkg-config
RUN apt-get update && apt-get install -y --no-install-recommends \
    pkg-config \
    libgobject-2.0-dev \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz0b \
    libfontconfig1 \
    libffi-dev \
    # Limpia el caché de apt para mantener la imagen ligera
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia e instala los requerimientos de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de tu aplicación
COPY . .

# Comando para iniciar tu aplicación (ajústalo si es necesario)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "$PORT"]
