import keras
from keras.layers import InputLayer, Conv2D, Flatten, Dense

model = keras.models.Sequential([
    InputLayer(input_shape=(16, 16, 1)),
    Conv2D(4, (3, 3), activation='relu'),
    Flatten(),
    Dense(150, activation='relu'),
    Dense(70, activation='relu'),
    Dense(9, activation='softmax')
])


model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
