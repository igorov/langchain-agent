FROM python:3.12-slim

ENV PYTHONUNBUFFERED True

# Variables de entorno con valores por defecto
ENV PORT 8080

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY . .

# Actualiza pip y setuptools
RUN pip install -U pip
RUN pip install -U setuptools

# Instala las dependencias desde requirements.txt, asegurándote de que psycopg2 sea reemplazado por psycopg2-binary
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

# CMD que ejecuta el script principal
CMD exec uvicorn src.main:app --host 0.0.0.0 --port ${PORT}