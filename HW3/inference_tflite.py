import time
import numpy as np
from tflite_runtime.interpreter import Interpreter
import cv2
from lite_lib import load_labels, set_input_tensor, classify_image

def main(label_path, model_path, img_name, augmentation):
    labels = load_labels(label_path)
    interpreter = Interpreter(model_path)
    print("Model Loaded Successfully.")

    interpreter.allocate_tensors()
    _, height, width, channel = interpreter.get_input_details()[0]['shape']
    print("Required input Shape ({}, {}, {})".format(height, width, channel))

    # load image for inference & preprocessing.
    # the data are normalized to 0~1 whrn training,
    # remenber to do it when inference
    image_show = cv2.imread(img_name)
    image = cv2.cvtColor(image_show, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (width, height))
    image = image / 255.0  # <- change the pixel range from 0~255 to 0~1

    # run inference on input image & measure the time spent
    results = classify_image(interpreter, image)  # inference first time
    start_time = time.time()
    results = classify_image(interpreter, image)  # inference second time
    stop_time = time.time()
    label_id, prob = results[0]

    # print predict result~
    print(50 * "=")
    print("Object in {} is a/an...".format(img_name))
    print("{}! Confidence={}".format(labels[label_id], prob))
    print(50 * "=")
    print("Time spend: {:.5f} sec.".format(stop_time - start_time))

    # show image
    cv2.imshow('img', image_show)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    label_path = 'model/catdog_label.txt'
    model_path = 'model/catdog_mobilenetv2.h5'
    img_name = 'catdog_subset/cat1.jpg'  # <- you can change to any other test sample in "cifar10_subset" folder
    
    for i in range(5):
        main(label_path, model_path, img_name, i)
        print('Next')