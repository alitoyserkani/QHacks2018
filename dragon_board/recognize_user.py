import cv2
import json
import sys
import requests
import os
#from ggts import gTTS

DEVICE_NUMBER = 0
IMAGE_FILE = "output.jpg"
API = "http://ec2-18-219-99-191.us-east-2.compute.amazonaws.com:5000/verify"
no_face = True

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

            # filename = sys/class/gpio/gpio36
            # os.system('./Electronics/turnOnGPIO.sh')
            # filename = sys/class/gpio/gpio12
            # os.system('./Electronics/turnOnGPIO.sh')

            k = raw_input("")
            if k == 'q':
                sys.exit(1)
            # else:
                # filename = ~/sys/class/gpio/gpio36
                # os.system('./Electronics/turnOnGPIO.sh')
                # filename = ~/sys/class/gpio/gpio12
                # os.system('./Electronics/turnOnGPIO.sh')
