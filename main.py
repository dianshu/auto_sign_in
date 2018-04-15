import os
from sign_in import SignIn
from params import exe_files
from time import sleep
import pyautogui as pg

def setUp():
    for exe_file in exe_files:
        os.startfile(exe_file)
    pos = None
    while pos is None:
        sleep(5)
        pos = pg.locateCenterOnScreen('start_appium.png')
    pg.click(*pos)
    sleep(20)
    os.system('nox_adb connect 127.0.0.1:62001')


def tearDown():
    for exe_file in exe_files:
        exe_name = os.path.split(exe_file)[-1]
        os.popen('TASKKILL /F /IM %s' % exe_name)


def main():
    try:
        setUp()
        SignIn().main()
    finally:
        tearDown()


if __name__ == '__main__':
    main()
