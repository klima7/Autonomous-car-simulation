import tensorflow as tf
from tensorflow.keras import datasets, layers, models

model = models.Sequential()

# # Conv 32x32x1 => 28x28x6.
# model.add(layers.Conv2D(filters=6, kernel_size=(5, 5), activation='relu', data_format='channels_last', input_shape=(24, 24, 1)))
#
# # Maxpool 28x28x6 => 14x14x6
# model.add(layers.MaxPooling2D((2, 2)))
#
# # Conv 14x14x6 => 10x10x16
# model.add(layers.Conv2D(16, (5, 5), activation='relu'))
#
# # Maxpool 10x10x16 => 5x5x16
# model.add(layers.MaxPooling2D((2, 2)))
#
# # Flatten 5x5x16 => 400
# model.add(layers.Flatten())
#
# # Fully connected 400 => 120
# model.add(layers.Dense(120, activation='relu'))
#
# # Fully connected 120 => 84
# model.add(layers.Dense(84, activation='relu'))
#
# # Dropout
# model.add(layers.Dropout(0.2))
#
# # Fully connected, output layer 84 => 43
# model.add(layers.Dense(9, activation='softmax'))

from keras.layers.core import Dense, Dropout, Activation
import keras

model = keras.models.Sequential([
keras.layers.Flatten(input_shape=(16*16,)),
keras.layers.Dense(150, activation="relu"),
keras.layers.Dense(70, activation="relu"),
keras.layers.Dense(9, activation="softmax")
])


model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
