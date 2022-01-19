import time
import RPi.GPIO as GPIO

R_PIN = 3 #LED的三原色腳位
G_PIN = 5
B_PIN = 15
Y_PIN = 11
Button_PIN = 13
sum = "0000"
times = 0

GPIO.setmode(GPIO.BOARD)

GPIO.setup(R_PIN, GPIO.OUT)
GPIO.setup(B_PIN, GPIO.OUT)
GPIO.setup(G_PIN, GPIO.OUT)
GPIO.setup(Y_PIN, GPIO.OUT)
GPIO.setup(Button_PIN, GPIO.IN)

def binary_addtion(input):
    b = "1"
    max_len = max(len(input), len(b))
    input = input.zfill(max_len)
    b = b.zfill(max_len)
    result = ''
    carry = 0
    for i in range(max_len - 1, -1, -1):
        r = carry
        r += 1 if input[i] == '1' else 0
        r += 1 if b[i] == '1' else 0
        result = ('1' if r % 2 == 1 else '0') + result
        carry = 0 if r < 2 else 1
    if carry != 0:
        result = '1' + result
    if result == "10000":
        result = "0000"
    return result

try:
    while True:
        if GPIO.input(Button_PIN) == GPIO.HIGH:
            times +=1
            sum = binary_addtion(sum)
            print('detect!', times, sum)
        if sum[0] == "1":
            GPIO.output(R_PIN, GPIO.HIGH)
        if sum[0] == "0":
            GPIO.output(R_PIN, GPIO.LOW)
        if sum[1] == "1":
            GPIO.output(G_PIN, GPIO.HIGH)
        if sum[1] == "0":
            GPIO.output(G_PIN, GPIO.LOW)
        if sum[2] == "1":
            GPIO.output(B_PIN, GPIO.HIGH)
        if sum[2] == "0":
            GPIO.output(B_PIN, GPIO.LOW)
        if sum[3] == "1":
            GPIO.output(Y_PIN, GPIO.HIGH)
        if sum[3] == "0":
            GPIO.output(Y_PIN, GPIO.LOW)
        time.sleep(0.3)
except KeyboardInterrupt:
    print("kb")
finally:
    GPIO.cleanup()












