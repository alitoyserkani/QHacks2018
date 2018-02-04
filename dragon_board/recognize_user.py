# from ggts import gTTS
from gpio_96boards import GPIO
import cv2
import json
import os
import requests
import sys
import time

DEVICE_NUMBER = 0
IMAGE_FILE = "output.jpg"
API = "http://ec2-18-219-99-191.us-east-2.compute.amazonaws.com:5000/verify"
no_face = True

GPIO_A = GPIO.gpio_id('GPIO_A')
GPIO_C = GPIO.gpio_id('GPIO_C')
GPIO_E = GPIO.gpio_id('GPIO_E')
GPIO_I = GPIO.gpio_id('GPIO_I')
GPIO_K = GPIO.gpio_id('GPIO_K')
light_pins = (
    (GPIO_A, 'out'),
)
gpioc = ((GPIO_C, 'out'),)
gpioe = ((GPIO_E, 'out'),)
gpioi = ((GPIO_I, 'out'),)
gpiok = ((GPIO_K, 'out'),)

steps = 0
direction = True


def stepper(xw):
    for x in range(xw):
        if steps == 0:
            with GPIO(gpioc) as gpio:
                gpio.digital_write(GPIO_C, GPIO.LOW)
            with GPIO(gpioe) as gpio:
                gpio.digital_write(GPIO_E, GPIO.LOW)
            with GPIO(gpioi) as gpio:
                gpio.digital_write(GPIO_I, GPIO.LOW)
            with GPIO(gpiok) as gpio:
                gpio.digital_write(GPIO_K, GPIO.HIGH)
        elif steps == 1:
            with GPIO(gpioc) as gpio:
                gpio.digital_write(GPIO_C, GPIO.LOW)
            with GPIO(gpioe) as gpio:
                gpio.digital_write(GPIO_E, GPIO.LOW)
            with GPIO(gpioi) as gpio:
                gpio.digital_write(GPIO_I, GPIO.HIGH)
            with GPIO(gpiok) as gpio:
                gpio.digital_write(GPIO_K, GPIO.HIGH)

        elif steps == 2:
            with GPIO(gpioc) as gpio:
                gpio.digital_write(GPIO_C, GPIO.LOW)
            with GPIO(gpioe) as gpio:
                gpio.digital_write(GPIO_E, GPIO.LOW)
            with GPIO(gpioi) as gpio:
                gpio.digital_write(GPIO_I, GPIO.HIGH)
            with GPIO(gpiok) as gpio:
                gpio.digital_write(GPIO_K, GPIO.LOW)

        elif steps == 3:
            with GPIO(gpioc) as gpio:
                gpio.digital_write(GPIO_C, GPIO.LOW)
            with GPIO(gpioe) as gpio:
                gpio.digital_write(GPIO_E, GPIO.HIGH)
            with GPIO(gpioi) as gpio:
                gpio.digital_write(GPIO_I, GPIO.HIGH)
            with GPIO(gpiok) as gpio:
                gpio.digital_write(GPIO_K, GPIO.LOW)

        elif steps == 4:
            with GPIO(gpioc) as gpio:
                gpio.digital_write(GPIO_C, GPIO.LOW)
            with GPIO(gpioe) as gpio:
                gpio.digital_write(GPIO_E, GPIO.HIGH)
            with GPIO(gpioi) as gpio:
                gpio.digital_write(GPIO_I, GPIO.LOW)
            with GPIO(gpiok) as gpio:
                gpio.digital_write(GPIO_K, GPIO.LOW)

        elif steps == 5:
            with GPIO(gpioc) as gpio:
                gpio.digital_write(GPIO_C, GPIO.HIGH)
            with GPIO(gpioe) as gpio:
                gpio.digital_write(GPIO_E, GPIO.HIGH)
            with GPIO(gpioi) as gpio:
                gpio.digital_write(GPIO_I, GPIO.LOW)
            with GPIO(gpiok) as gpio:
                gpio.digital_write(GPIO_K, GPIO.LOW)

        elif steps == 6:
            with GPIO(gpioc) as gpio:
                gpio.digital_write(GPIO_C, GPIO.HIGH)
            with GPIO(gpioe) as gpio:
                gpio.digital_write(GPIO_E, GPIO.LOW)
            with GPIO(gpioi) as gpio:
                gpio.digital_write(GPIO_I, GPIO.LOW)
            with GPIO(gpiok) as gpio:
                gpio.digital_write(GPIO_K, GPIO.LOW)
        elif steps == 7:
            with GPIO(gpioc) as gpio:
                gpio.digital_write(GPIO_C, GPIO.HIGH)
            with GPIO(gpioe) as gpio:
                gpio.digital_write(GPIO_E, GPIO.LOW)
            with GPIO(gpioi) as gpio:
                gpio.digital_write(GPIO_I, GPIO.LOW)
            with GPIO(gpiok) as gpio:
                gpio.digital_write(GPIO_K, GPIO.HIGH)
        else:
            with GPIO(gpioc) as gpio:
                gpio.digital_write(GPIO_C, GPIO.LOW)
            with GPIO(gpioe) as gpio:
                gpio.digital_write(GPIO_E, GPIO.LOW)
            with GPIO(gpioi) as gpio:
                gpio.digital_write(GPIO_I, GPIO.LOW)
            with GPIO(gpiok) as gpio:
                gpio.digital_write(GPIO_K, GPIO.LOW)


def set_direction():
    global steps
    steps += direction

    if steps > 7:
        steps = 0
    elif steps < 0:
        steps = 7


def open_door():
    global direction
    direction = 1
    for step in range(3):
        time.sleep(0.5)
        stepper(1)
        set_direction()
    stop_door()


def close_door():
    global direction
    direction = -1
    for step in range(3):
        time.sleep(0.5)
        stepper(1)
        set_direction()
    stop_door()


def stop_door():
    with GPIO(gpioc) as gpio:
        gpio.digital_write(GPIO_C, GPIO.LOW)
    with GPIO(gpioe) as gpio:
        gpio.digital_write(GPIO_E, GPIO.LOW)
    with GPIO(gpioi) as gpio:
        gpio.digital_write(GPIO_I, GPIO.LOW)
    with GPIO(gpiok) as gpio:
        gpio.digital_write(GPIO_K, GPIO.LOW)


def turn_on(gpio):
    gpio.digital_write(GPIO_A, GPIO.HIGH)


def turn_off(gpio):
    gpio.digital_write(GPIO_A, GPIO.LOW)


def main():
    while no_face:
        vc = cv2.VideoCapture(DEVICE_NUMBER)
        retVal, frame = vc.read()
        small = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        cv2.imwrite(IMAGE_FILE, small)
        vc.release()

        print("Done reading image.")

        response = requests.post(API, files={
            "image": open(
                '/home/linaro/haven/dragon_board/output.jpg', 'r')})

        print("Received web response.")

        if response.status_code == 200:
            user = json.loads(response.text)['user']
            confidence = json.loads(response.text)['confidence']

            if confidence > 0.97:
                # home_actions(user)
                first = user.split("-")[0].title()
                last = user.split("-")[1].title()
                print(first + " " + last + " recognised.")
                # text = "Welcome home " + first + " " + last)
                # tts = gTTS(text, lang='en')
                # tts.save("welcome_msg.mp3")
                # os.system("mp321 welcome_msg.mp3")

                with GPIO(light_pins) as gpio:
                    turn_on(gpio)
                open_door()
                time.sleep(3)
                close_door()

                # filename = sys/class/gpio/gpio12
                # os.system('./Electronics/turnOnGPIO.sh')

                k = raw_input("")
                if k == 'q':
                    with GPIO(light_pins) as gpio:
                        turn_off(gpio)
                    sys.exit(1)
                else:
                    with GPIO(light_pins) as gpio:
                        turn_off(gpio)
                    # filename = ~/sys/class/gpio/gpio12
                    # os.system('./Electronics/turnOnGPIO.sh')


if __name__ == "__main__":
    main()
