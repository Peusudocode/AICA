import cv2
import random
import numpy as np
img_name = 'catdog_subset/cat2.jpg'
img = cv2.imread(img_name)
horizon_flip_image = cv2.flip(img, 1) #水平翻轉
cv2.imwrite("horizon_flip_image.jpg", horizon_flip_image)
vertical_flip_image = cv2.flip(img, 0) #垂直翻轉
cv2.imwrite("vertical_flip_image.jpg", vertical_flip_image)


def gaussian_noise(img, mean=0, sigma=0.1):
    # int -> float (標準化)
    img = img / 255
    # 隨機生成高斯 noise (float + float)
    noise = np.random.normal(mean, sigma, img.shape)
    # noise + 原圖
    gaussian_out = img + noise
    # 所有值必須介於 0~1 之間，超過1 = 1，小於0 = 0
    gaussian_out = np.clip(gaussian_out, 0, 1)

    # 原圖: float -> int (0~1 -> 0~255)
    gaussian_out = np.uint8(gaussian_out * 255)
    return gaussian_out


gaussian_noise_image = gaussian_noise(img,0,0.1) #高斯噪點
cv2.imwrite("gaussian_noise_image.jpg", gaussian_noise_image)


gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh_img = cv2.threshold(gray_img,127,255,cv2.THRESH_BINARY) #二值化(黑白)
cv2.imwrite("thresh_img.jpg", thresh_img)


#salt and pepper noise
def add_noise(img):
    # Getting the dimensions of the image
    row, col = img.shape

    # Randomly pick some pixels in the
    # image for coloring them white
    # Pick a random number between 300 and 10000
    number_of_pixels = random.randint(300, 10000)
    for i in range(number_of_pixels):
        # Pick a random y coordinate
        y_coord = random.randint(0, row - 1)

        # Pick a random x coordinate
        x_coord = random.randint(0, col - 1)

        # Color that pixel to white
        img[y_coord][x_coord] = 255

    # Randomly pick some pixels in
    # the image for coloring them black
    # Pick a random number between 300 and 10000
    number_of_pixels = random.randint(300, 10000)
    for i in range(number_of_pixels):
        # Pick a random y coordinate
        y_coord = random.randint(0, row - 1)

        # Pick a random x coordinate
        x_coord = random.randint(0, col - 1)

        # Color that pixel to black
        img[y_coord][x_coord] = 0
    return img


salt_and_pepper_noise_img = add_noise(gray_img) #salt and pepper noise
cv2.imwrite("salt_and_pepper_noise_img.jpg", salt_and_pepper_noise_img)

height, width, _ = img.shape
start_point = (0, 0)
end_point = (80, 300)
color = (0, 0, 0)
thickness = -1
cover_image = cv2.rectangle(img, start_point, end_point, color, thickness)  #部分遮蓋
cv2.imwrite("cover_image.jpg", cover_image)
print(height, width)