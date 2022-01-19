import time
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
import cv2


def load_labels(path):
    with open(path, 'r') as f:
        return {i: line.strip() for i, line in enumerate(f.readlines())}


def main(label_path, model_path, img_name):
    labels = load_labels(label_path)
    model = load_model(model_path, compile=False)
    print("Model Loaded Successfully.")

    _, height, width, channel = model.layers[0].output_shape[0]
    print("Required input Shape ({}, {}, {})".format(height, width, channel))

    # load image for inference
    image_show = cv2.imread(img_name)
    image = cv2.cvtColor(image_show, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (width, height))
    image = image / 255.0
    image = np.reshape(image, (1, height, width, channel))

    # run inference on input image
    results = model.predict(image)[0]  # inference first time
    start_time = time.time()
    results = model.predict(image)[0]  # inference second time
    stop_time = time.time()
    label_id = np.argmax(results)
    prob = results[label_id]

    # print predict result~
    print(50 * "=")
    print("Object in {} is a/an...".format(img_name))
    print("{}! Confidence={}".format(labels[label_id], prob))
    print(50 * "=")
    print("Time spend: {:.5f} sec.".format(stop_time - start_time))


if __name__ == "__main__":
    print(tf.__version__)
    label_path = 'model/catdog_label.txt'
    model_path = 'model/catdog_mobilenetv2.h5'
    img_name = 'catdog_subset/cat1.jpg'  # <- you can change to any other test sample in "cifar10_subset" folder
    main(label_path, model_path, img_name)
    print('Bye')