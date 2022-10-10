import pyautogui
import time

while 1:
    try:
        print(pyautogui.position())
        time.sleep(1)
    except:
        break
