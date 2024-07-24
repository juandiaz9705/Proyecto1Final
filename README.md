# Proyecto1Final
Entrega proyecto final módulo #1

Requisitos Previos.

1. Tener Docker Instalado.
2. Clonar el repositorio: git clone https://github.com/juandiaz9705/Proyecto1Final.git


Paso a paso
1. Construir la imagen Docker: docker build -t detector:neumonia .
2. Construir la variable display en linux: export DISPLAY=:0
3. Ejecutar el contenedor: docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix detector:neumonia python3 detector_neumonia.py


Estudiante:
Juan Diego Díaz Guzmán

