import cv2
import json
import sys
import requests
import os
import time

from gpio_96boards import GPIO
#from ggts import gTTS

DEVICE_NUMBER = 0
IMAGE_FILE = "output.jpg"
API = "http://ec2-18-219-99-191.us-east-2.compute.amazonaws.com:5000/verify"
no_face = True

GPIO_A = GPIO.gpio_id('GPIO_A')
pins = (
     (GPIO_A, 'out'),
)


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
                
                with GPIO(pins) as gpio:
                    turn_on(gpio)
                # filename = sys/class/gpio/gpio12
                # os.system('./Electronics/turnOnGPIO.sh')

                k = raw_input("")
                if k == 'q':
                    with GPIO(pins) as gpio:
                        turn_off(gpio)
                    sys.exit(1)
                else:
                    with GPIO(pins) as gpio:
                        turn_off(gpio)
                    # filename = ~/sys/class/gpio/gpio12
                    # os.system('./Electronics/turnOnGPIO.sh')

if __name__ == "__main__":
    main()

