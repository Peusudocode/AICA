import time
import numpy as np
from tflite_runtime.interpreter import Interpreter
import cv2
from lite_lib import load_labels, set_input_tensor, classify_image

def gaussian_noise(img, mean=0, sigma=0.1):
    # 隨機生成高斯 noise (float + float)
    noise = np.random.normal(mean, sigma, img.shape)
    # noise + 原圖
    gaussian_out = img + noise
    # 所有值必須介於 0~1 之間，超過1 = 1，小於0 = 0
    gaussian_out = np.clip(gaussian_out, 0, 1)
    
    # 原圖: float -> int (0~1 -> 0~255)
    gaussian_out = np.uint8(gaussian_out*255)
    # noise: float -> int (0~1 -> 0~255)
    noise = np.uint8(noise*255)
    
    return gaussian_out

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
    
    if augmentation ==0:
        image=cv2.flip(image,1) #horizatal
    elif augmentation ==1:
        image=cv2.flip(image,0) #vertical
    elif augmentation ==2:
        image=gaussian_noise(image,0,0.5)
    elif augmentation ==3:
        image=cv2.rectangle(image,(0,0),(int(image.shape[0]/2),int(image.shape[0]/2)),(0,0,0),-1)
    elif augmentation ==4:
        ret, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

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
    label_path = 'model/cifar10_label.txt'
    model_path = 'model/cifar10_mobilenetv2.tflite'
    img_name = 'catdog_subset/cat2.jpg'  # <- you can change to any other test sample in "cifar10_subset" folder
    
    for i in range(5):
        main(label_path, model_path, img_name, i)
        print('Next')