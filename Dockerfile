FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema optimizadas
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copiar requirements primero
COPY requirements.txt .
RUN pip install --upgrade pip

# Instalar dependencias básicas primero
RUN pip install --no-cache-dir \
    flask==2.3.3 \
    flask-cors==4.0.0 \
    gunicorn==21.2.0 \
    pandas==2.0.3 \
    numpy==1.24.3

# Instalar dependencias de ML por separado (manejo de errores)
RUN pip install --no-cache-dir scikit-learn==1.3.0 || echo "scikit-learn installation warning"
RUN pip install --no-cache-dir opencv-python-headless==4.8.1.78 || echo "opencv installation warning"
RUN pip install --no-cache-dir ultralytics==8.0.186 || echo "ultralytics installation warning"
RUN pip install --no-cache-dir face-recognition==1.3.0 || echo "face-recognition installation warning"

# Instalar el resto
RUN pip install --no-cache-dir -r requirements.txt

# Descargar datos de NLTK (opcional, puede fallar)
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('vader_lexicon')" 2>/dev/null || echo "NLTK download skipped"

# Copiar aplicación
COPY . .

# Crear directorios
RUN mkdir -p api/db api/models
RUN echo '[]' > api/db/users_db.json

EXPOSE 5000

ENV FLASK_ENV=production
ENV PYTHONPATH=/app

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "application:application"]