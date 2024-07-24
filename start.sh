#!/bin/bash

# Iniciar el servidor VNC sin contraseña
x11vnc -nopw -display :0 -forever &

# Iniciar el entorno gráfico con fluxbox
fluxbox &

# Ejecutar la aplicación con un entorno gráfico virtual
xvfb-run -a python detector_neumonia.py
