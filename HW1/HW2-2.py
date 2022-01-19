import time
import sys
import cv2
import random
time_start = time.time() #開始計時
def mosaic_effect(img, x, y, w, h):
    new_img = img.copy()
    size = 10    # 馬賽克大小
    for i in range(x + size, (x + w) - 1 - size, size):
        for j in range(y + size, (y + h) - 1 - size, size):
            i_rand = random.randint(i - size, i)
            j_rand = random.randint(j - size, j)
            new_img[i - size:i + size, j - size:j + size] = img[i_rand, j_rand, :]
    return new_img

capture = cv2.VideoCapture('example.mp4')

fps = int(capture.get(cv2.CAP_PROP_FPS))    # Frame rate of the video
total_frame = int (capture.get(cv2.CAP_PROP_FRAME_COUNT))   # Amount of frames
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, fps, (width, height))

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

print('Start Processing...\n')

for i in range(total_frame):
    # Erase the last line in terminal
    sys.stdout.write(CURSOR_UP_ONE)
    sys.stdout.write(ERASE_LINE)
    print('progress: {} %'.format(round(((i + 1) / total_frame) * 100, 2)))

    status, frame = capture.read()  # Read the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    # Convert to grayscale
    faces = face_cascade.detectMultiScale(gray, 1.1, 4) # Detect the faces

    for (x, y, w, h) in faces:
        # Draw the rectangle around each face
        frame = mosaic_effect(frame, x, y, w, h)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    out.write(frame)

capture.release()

time_end = time.time()

time_c= time_end - time_start
print('time cost', time_c, 's')