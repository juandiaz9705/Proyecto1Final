# Usa la imagen base de TensorFlow con soporte para GPU
FROM tensorflow/tensorflow:2.12.0-gpu

# Configura el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app

# Instala dependencias del sistema
RUN apt-get update && \
    apt-get install -y \
    python3-tk \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Define el comando por defecto para ejecutar la aplicación
CMD ["python", "detector_neumonia.py"]
