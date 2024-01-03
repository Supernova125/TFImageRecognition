import tensorflow as tf
import matplotlib.pyplot as plt
import pathlib

from keras.utils import image_dataset_from_directory
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Flatten, Rescaling
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import RandomRotation, RandomZoom, RandomFlip
from keras.losses import SparseCategoricalCrossentropy

import pathlib
from toml import load as tload

config = tload('config.toml')

data_dir = pathlib.Path(config["batcher"]["batch_folder_name"]).with_suffix("")
image_count = len(list(data_dir.glob('*/*.jpg')))
print(str(image_count) + " images found")

batch_size = config["training"]["batch_size"]
img_height = config["training"]["img_height"]
img_width = config["training"]["img_width"]

train_ds = image_dataset_from_directory(
    data_dir,
    validation_split=config["training"]["validation_split"],
    subset="training",
    seed=config["training"]["seed"],
    image_size=(img_height, img_width),
    batch_size=batch_size)

val_ds = image_dataset_from_directory(
    data_dir,
    validation_split=config["training"]["validation_split"],
    subset="validation",
    seed=config["training"]["seed"],
    image_size=(img_height, img_width),
    batch_size=batch_size)

class_names = train_ds.class_names
print(class_names)

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

num_classes = len(class_names)

# Augmentation against overfitting
data_augmentation = Sequential(
    [
    RandomFlip("horizontal",
                      input_shape=(img_height,
                                  img_width,
                                  3)),
    RandomRotation(0.1),
    RandomZoom(0.1),
    ]
)

# already includes dropout!
model = Sequential([
    data_augmentation,
    Rescaling(1./255),
    Conv2D(16, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Conv2D(32, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Conv2D(64, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Dropout(0.2),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(num_classes, name="outputs")
])

model.compile(optimizer='adam',
              loss=SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# Training!!
epochs = config["training"]["epochs"]
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs
)

model.summary()

model.save(config["training"]["result_file_name"])

# Visuals
if config["training"]["final_stats"]:
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    
    epochs_range = range(epochs)
    
    plt.figure(figsize=(8, 8))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')
    
    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.show()