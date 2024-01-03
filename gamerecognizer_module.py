import tensorflow as tf
from PIL import Image
import keras

def load_model(path: str):
    """
    Loads a Keras model from a given file path.

    Args:
        path (str): The file path to the Keras model.

    Returns:
        The loaded Keras model instance.
    """
    keras_model = keras.models.load_model(path)
    return keras_model

def predict(model: keras.models.Model, image_path: str) -> tuple:
    """
    Predicts the class of an image using a given Keras model.

    Args:
        model (keras.models.Model): The Keras model to use for prediction.
        image_path (str): The path to the image to predict the class of.

    Returns:
        Tuple of prediction (as integer) and score (as float).
    """
    img = Image.open(image_path).resize((144, 256))
    img = img.convert('RGB')
    
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    
    prediction = model.predict(img_array)
    score = tf.nn.softmax(prediction)
    return (prediction, score)