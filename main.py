import numpy as np
import cv2
import pytesseract
from pynput import mouse
import pyscreenshot as ImageGrab


start_x, end_x = -1, -1
start_y, end_y = -1, -1


def on_click(x, y, button, pressed):
    global start_x, start_y
    global end_x, end_y
    if pressed:
        start_x = x
        start_y = y
    else:
        end_x = x
        end_y = y
    if not pressed:
        return False


with mouse.Listener(
        on_click=on_click) as listener:
    listener.join()

listener = mouse.Listener(
    on_click=on_click
)
listener.start()

img = ImageGrab.grab(bbox=(start_x, start_y, end_x, end_y))
img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
threshold_image = cv2.threshold(
    gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

custom_config = r'--oem 3 --psm 6'
details = pytesseract.image_to_data(
    threshold_image, output_type=pytesseract.Output.DICT, config=custom_config)

parse_text = []
for word in details['text']:
    if word != '':
        parse_text.append(word)

print(' '.join(parse_text))
