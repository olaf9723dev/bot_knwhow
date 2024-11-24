import re
import os
import cv2
import csv
import json
import time
import random
import sqlite3
import requests
import pyautogui
import numpy as np
from faker import Faker
from pywinauto import Desktop, Application
from pywinauto.keyboard import send_keys
from pynput.mouse import Controller, Button
from emailer import Emailer

class Signin:
    def __init__(self, username, password):
        pass

    def start(self):
        app = Application().start(r'"C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory=Default')
        time.sleep(3)
        windows = Desktop(backend="uia").windows()
        print('Windows with "Google Chrome" in the title:')
        for window in windows:
            title = window.window_text()
            if "Google Chrome" in title and "New Tab" in title:
                print(f"- {title}")
                # Focus on New Chrome Browser window
                window.set_focus()
                window.maximize()

                time.sleep(1)
                # Type target url
                send_keys("^l")
                send_keys("https://www.mtndewgaming.com/signin{ENTER}")
                time.sleep(3)
                send_keys("^l")
                send_keys("{ENTER}")

                break