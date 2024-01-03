import tensorflow as tf
import numpy as np
import sys
from PIL import Image
import keras
import os
from toml import load as tload

config = tload('config.toml')

KERAS_MODEL_PATH = "gamerecognizer.keras"

img_height = 144
img_width = 256

keras_model = keras.models.load_model(KERAS_MODEL_PATH)

class_names = os.listdir('game_images') 

img = Image.open(sys.argv[1]).resize((img_height, img_width))
img = img.convert('RGB')

img_array = tf.keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)

prediction = keras_model.predict(img_array)
score_lite = tf.nn.softmax(prediction)

print(
    "This image most likely belongs to {} with a {:.2f} percent confidence."
    .format(class_names[np.argmax(score_lite)], 100 * np.max(score_lite))
)
input()