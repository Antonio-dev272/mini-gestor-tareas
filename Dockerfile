# Usa una imagen base de Python ligera. Python 3.9 es una buena opción.
FROM python:3.9-slim-buster

# Establece el directorio de trabajo dentro del contenedor.
# Aquí es donde se copiará tu código.
WORKDIR /app

# Copia el archivo de requisitos.txt al directorio de trabajo y instala las dependencias.
# Esto es crucial para que Flask, pytest, etc., estén disponibles.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el resto del código fuente de tu proyecto al directorio de trabajo en el contenedor.
COPY . .

# Expone el puerto 5000, que es el puerto en el que Flask escuchará.
EXPOSE 5000

# Define una variable de entorno FLASK_APP para que Flask sepa cuál es tu aplicación principal.
ENV FLASK_APP=app.py

# Este es el comando que se ejecutará cuando el contenedor se inicie.
# Inicia la aplicación Flask y la hace accesible en todas las interfaces de red del contenedor (0.0.0.0).
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]