Hola! Bienvenido a la herramienta para la detección rápida de neumonía.

A continuación le explicaremos cómo empezar a utilizarla

Requerimientos necesarios para el funcionamiento:

- Descargue python de la siguiente ruta: https://www.python.org/downloads/windows/

INSTRUCCIONES PARA CORRER EL CONTENEDOR DEL PROYECTO
1. Tener Instalado Docker.
2. Tener xmin instalado.
3. Ejecutar la imagen: docker run -it --rm judiazg/detector_neumonia
4. Verificación del montaje.
docker run -it --rm \ -e DISPLAY=$DISPLAY \ -v /tmp/.X11-unix:/tmp/.X11-
unix \ judiazg/detector_neumonia
5. Repositorio de GitHub: https://github.com/juandiaz9705/Proyecto1Final.git
Consideraciones:
Nota:
1. se debe descargar el archivo de la predicción de la siguiente ruta:
https://drive.google.com/drive/folders/1GrdtsYRcOzQJdkgkfpspNfzNii8XX18T?usp=shari
ng ya que este archivo es importante para generar la predicción.
2. Una vez descargado el archivo WilhemNet_86.h5, se debe modificar la línea 5 del archivo
load_model.py para actualizar la ruta del modelo. En mi caso, esta línea apunta a mi entorno
local: model_cnn = model_path = '/app/WilhemNet_86.h5' # Ruta dentro del contenedor
DockerDebes cambiar esta ruta para que apunte a la ubicación donde se guardó el archivo
del modelo descargado

- Abra la consola del sistema y ejecute las siguientes líneas
	git clone https://github.com/juandiaz9705/Proyecto1Final.git

	pip install -r requirements.txt

	python detector_neumonia.py
----------------------------------------------------------------------------------

Uso de la herramienta:

- Ingrese la cédula del paciente en la caja de texto
- Presione el botón 'Cargar Imagen', seleccione la imagen del explorador de archivos
del computador
- Presione el botón 'Predecir' y espere unos segundos hasta que observe los resultados
- Presione el botón 'Guardar' para almacenar la información del paciente en un archivo excel
con extensión .csv
- Presione el botón 'PDF' para descargar un archivo PDF con la información desplegada en la interfaz
- Presión el botón 'Limpiar' si desea cargar una nueva imagen
