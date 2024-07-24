import tensorflow as tf

def model():
    try:
        model_path = '/app/WilhemNet_86.h5'  # Ruta dentro del contenedor Docker
        model_cnn = tf.keras.models.load_model(model_path)
        return model_cnn
    except OSError as e:
        print(f"Error loading model: {e}")
        return None
