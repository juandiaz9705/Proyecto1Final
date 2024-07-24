import cv2
import numpy as np

def preprocess(array):
    # Verificar si la imagen tiene 3 canales (color) y convertirla a escala de grises si es necesario
    if len(array.shape) == 3 and array.shape[2] == 3:
        array = cv2.cvtColor(array, cv2.COLOR_BGR2GRAY)
    elif len(array.shape) == 2:
        # La imagen ya está en escala de grises, no hacer nada
        pass
    else:
        raise ValueError("Formato de imagen no soportado")
    
    # Redimensionar la imagen al tamaño necesario para el modelo (suponiendo 512x512)
    array = cv2.resize(array, (512, 512), interpolation=cv2.INTER_AREA)
    
    # Aplicar CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
    array = clahe.apply(array)
    
    # Normalizar la imagen
    array = array / 255.0
    
    # Expandir las dimensiones para que sea compatible con el modelo
    array = np.expand_dims(array, axis=-1)  # Añadir canal de color si es necesario (para modelos que esperan 4D: batch, height, width, channels)
    array = np.expand_dims(array, axis=0)   # Añadir la dimensión del batch

    return array
