import math
import os
import random
from enum import Enum
import cv2
import numpy as np
import tensorflow as tf
from keras.models import load_model
from time import time

from nn.signn import model


class SignType(Enum):
    STOP = 0
    WALKWAY = 1
    ROUNDABOUT = 2
    PARKING = 3
    LIMIT = 4
    ONEWAY = 5
    DEADEND = 6
    TRAFFIC_LIGHTS = 7
    REVERSED = 8
    UNKNOWN = 9


def load_images_from_dir(directory, max_count=math.inf):
    names = []

    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            names.append(filename)

    images = []
    count = 0

    while names:
        if count >= max_count:
            break
        name = random.choice(names)
        names.remove(name)
        image = cv2.imread(os.path.join(directory, name))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = image.astype(np.float32) / 255
        images.append(image)
        count += 1

    return images


def load_training_data(directory):
    rev_count = 100

    stop = load_images_from_dir(os.path.join(directory, 'stop', 'normal'), max_count=600)
    walkway = load_images_from_dir(os.path.join(directory, 'walkway', 'normal'))
    roundabout = load_images_from_dir(os.path.join(directory, 'roundabout', 'normal'))
    parking = load_images_from_dir(os.path.join(directory, 'parking', 'normal'))
    limit = load_images_from_dir(os.path.join(directory, 'limit', 'normal'))
    oneway = load_images_from_dir(os.path.join(directory, 'oneway', 'normal'))
    deadend = load_images_from_dir(os.path.join(directory, 'deadend', 'normal'))
    lights = load_images_from_dir(os.path.join(directory, 'lights', 'normal'))
    reversed = [
        *load_images_from_dir(os.path.join(directory, 'stop', 'reversed'), max_count=rev_count),
        *load_images_from_dir(os.path.join(directory, 'walkway', 'reversed'), max_count=rev_count),
        *load_images_from_dir(os.path.join(directory, 'roundabout', 'reversed'), max_count=rev_count),
        *load_images_from_dir(os.path.join(directory, 'parking', 'reversed'), max_count=rev_count),
        *load_images_from_dir(os.path.join(directory, 'limit', 'reversed'), max_count=rev_count),
        *load_images_from_dir(os.path.join(directory, 'oneway', 'reversed'), max_count=rev_count),
        *load_images_from_dir(os.path.join(directory, 'deadend', 'reversed'), max_count=rev_count),
    ]

    print('reversed', len(reversed))

    data = {
        SignType.STOP: stop,
        SignType.WALKWAY: walkway,
        SignType.ROUNDABOUT: roundabout,
        SignType.PARKING: parking,
        SignType.LIMIT: limit,
        SignType.ONEWAY: oneway,
        SignType.DEADEND: deadend,
        SignType.TRAFFIC_LIGHTS: lights,
        SignType.REVERSED: reversed
    }

    return data


def create_training_sets(data):
    rows = []

    for label, images in data.items():
        for image in images:
            row = (image, label)
            rows.append(row)

    random.shuffle(rows)

    images = np.array([row[0] for row in rows])
    labels = np.array([row[1].value for row in rows])
    labels = tf.one_hot(labels, 9)

    images = np.reshape(images, (images.shape[0], 16, 16, 1))
    return images, labels


data = load_training_data('images/gray16')
images, labels = create_training_sets(data)

# model = load_model('model.h5')
model.fit(images, labels, batch_size=16, epochs=50, verbose=1)
model.save('model.h5')

start = time()
print(np.argmax(model.predict(images[0:1])[0]))
print(time() - start)