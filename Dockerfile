# Usa una imagen base de Python específica (Debian 12 Bookworm)
FROM python:3.12-slim-bookworm

# Variables de entorno recomendadas
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala el conjunto COMPLETO de dependencias de desarrollo para WeasyPrint
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    libcairo2-dev \
    libpango1.0-dev \
    libgdk-pixbuf-2.0-dev \
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
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
