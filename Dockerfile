FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema para todos los paquetes de ML
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    wget \
    software-properties-common \
    cmake \
    git \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libopencv-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero (para aprovechar cache de Docker)
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Descargar datos de NLTK
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('vader_lexicon')"

# Copiar código de la aplicación
COPY . .

# Crear directorios necesarios
RUN mkdir -p api/db api/models

# Exponer puerto
EXPOSE 5000

# Variables de entorno
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Comando de inicio con timeout extendido para procesamiento de imágenes
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "--workers", "2", "application:application"]