import pytest
import os
import numpy as np
from read_img import read_dicom_file
from PIL import Image

def test_read_dicom_file():
    # Ruta a una imagen de prueba en formato DICOM
    test_image_path = r'C:\UAO\UAO-Neumonia\sample-images\DICOM\viral (2).dcm'
    
    # Verifica que la imagen existe
    assert os.path.exists(test_image_path), "La imagen de prueba no existe."
    
    # Lee la imagen usando la función
    img_RGB, img2show = read_dicom_file(test_image_path)
    
    # Verifica que las salidas no sean None
    assert img_RGB is not None, "La función no debe retornar None."
    assert img2show is not None, "La función no debe retornar None."
    
    # Verifica que la salida sea un arreglo numpy
    assert isinstance(img_RGB, np.ndarray), "La salida debe ser un arreglo numpy."
    
    # Verifica las dimensiones del arreglo (pueden variar, por lo que no se verifica el tamaño exacto)
    assert len(img_RGB.shape) == 3, "La imagen no tiene las dimensiones esperadas."
    
    # Guarda la imagen procesada para verificación manual
    img_save_path = r'C:\UAO\UAO-Neumonia\test_output\processed_image.png'
    os.makedirs(os.path.dirname(img_save_path), exist_ok=True)
    Image.fromarray(img_RGB).save(img_save_path)
    print(f"Imagen procesada guardada en: {img_save_path}")

if __name__ == '__main__':
    pytest.main()
