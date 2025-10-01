# Usar imagen base oficial de Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY backend/ ./backend/
# Copiar frontend bueno utilizado por app.py
COPY www.molpi.com.ar/ ./www.molpi.com.ar/

# Copiar base de datos
COPY backend/molpi.db ./backend/molpi.db

# Crear directorio para archivos estáticos
RUN mkdir -p ./backend/static

# Exponer puerto
EXPOSE 8080

# Variables de entorno
ENV FLASK_APP=backend/app.py
ENV FLASK_ENV=production
ENV PORT=8080
ENV HOST=0.0.0.0

# Comando para ejecutar la aplicación (gunicorn en producción, fallback a python)
ENV WEB_CONCURRENCY=1
CMD ["sh", "-c", "if command -v gunicorn >/dev/null 2>&1; then gunicorn -w ${WEB_CONCURRENCY} -b 0.0.0.0:${PORT:-8080} backend.app:app; else python backend/app.py; fi"]
