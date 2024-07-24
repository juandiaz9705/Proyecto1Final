import cv2
import numpy as np
import preprocess_img
import load_model
from tensorflow.keras import backend as K
import tensorflow as tf

tf.compat.v1.disable_eager_execution()
tf.compat.v1.experimental.output_all_intermediates(True)

def grad_cam(array): 
    # Preprocesar la imagen de entrada
    img = preprocess_img.preprocess(array)
    
    # Cargar el modelo
    model = load_model.model()
    
    # Realizar predicciones
    preds = model.predict(img)
    argmax = np.argmax(preds[0])
    
    # Obtener la capa de convolución y gradientes
    output = model.output[:, argmax]
    last_conv_layer = model.get_layer('conv10_thisone')  # Reemplazar con el nombre correcto
    grads = K.gradients(output, last_conv_layer.output)[0]
    pooled_grads = K.mean(grads, axis=(0, 1, 2))
    
    # Crear una función para obtener los gradientes y la salida de la capa de convolución
    iterate = K.function([model.input], [pooled_grads, last_conv_layer.output[0]])
    pooled_grads_value, conv_layer_output_value = iterate(img)
    
    # Aplicar gradientes a la salida de la capa de convolución
    conv_layer_output_value = np.squeeze(conv_layer_output_value)  # Eliminar dimensiones singleton
    for filters in range(conv_layer_output_value.shape[-1]):
        conv_layer_output_value[:, :, filters] *= pooled_grads_value[filters]
    
    # Crear el heatmap
    heatmap = np.mean(conv_layer_output_value, axis=-1)
    heatmap = np.maximum(heatmap, 0)  # ReLU
    heatmap /= np.max(heatmap)  # Normalizar
    heatmap = cv2.resize(heatmap, (array.shape[1], array.shape[0]))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    
    # Redimensionar la imagen original para que coincida con el tamaño del heatmap
    img2 = cv2.resize(array, (array.shape[1], array.shape[0]))
    
    # Verificar las dimensiones antes de la superposición
    print("Dimensiones de img2:", img2.shape)
    print("Dimensiones de heatmap:", heatmap.shape)
    
    # Crear la imagen superpuesta
    hif = 0.8
    transparency = heatmap * hif
    transparency = transparency.astype(np.uint8)
    superimposed_img = cv2.addWeighted(img2, 0.6, transparency, 0.4, 0)
    
    return superimposed_img[:, :, ::-1]  # Convertir de BGR a RGB
