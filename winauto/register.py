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

SITE_URL = "https://www.mtndewgaming.com/register"
mouse = Controller()

class Register:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("mtn.db")
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        
        self.fakers = dict()

        self.index = 0
        
        self.cursor.execute("SELECT * FROM tb_fakers WHERE used = 'false'")
        rows = self.cursor.fetchall()
        self.fakers_info = rows
        
        
        with open("uszips.csv", mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.uszips_info = [row for row in reader]


    def start(self, email, index):
        register_info = dict()
        app = Application().start(r'"C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory=Default')
        time.sleep(3)
        windows = Desktop(backend="uia").windows()
        print('Windows with "Google Chrome" in the title:')
        for window in windows:
            title = window.window_text()
            print(title)
            if "Google Chrome" in title and "New Tab" in title:
                print(f"- {title}")
                # Focus on New Chrome Browser window
                window.set_focus()
                window.maximize()

                time.sleep(1)
                # Type target url
                send_keys("^l")
                send_keys("https://www.mtndewgaming.com/register{ENTER}")
                time.sleep(3)
                send_keys("^l")
                send_keys("{ENTER}")
                time.sleep(15)
                current_title = window.window_text()

                if "Attention Required!" in current_title:
                    window.close()
                    register_info["registered"] = "false"
                    return register_info

                while "Just a moment" in current_title:
                    print('Captcha Page...')
                    time.sleep(1)
                    self.gui_click("captcha0.png")
                    current_title = window.window_text()
                
                current_title = window.window_text()

                if "Attention Required!" in current_title:
                    window.close()
                    register_info["registered"] = "false"
                    return register_info

            #     # person_info = self.generate_person_info()
                person_info = self.fakers_info[index]
                print(person_info)

                register_info['first_name'] = person_info['first_name']
                register_info['last_name'] = person_info['last_name']
                register_info['email_address'] = email['email']
                register_info['account_password'] = "qwer1234QWER!@#$"
                register_info['address'] = person_info['address']
                register_info['city'] = person_info['city']
                register_info['state'] = person_info['state']
                register_info['zip_code'] = self.get_valid_zipcode(register_info['state'])
                register_info['phone_number'] = person_info['phone']
                register_info['birth'] = person_info['birth']

                window.type_keys("{TAB}" * 4)
                send_keys(register_info['first_name'])
                window.type_keys("{TAB}")
                send_keys(register_info['last_name'])
                window.type_keys("{TAB}")
                send_keys(register_info['email_address'])
                window.type_keys("{TAB}")
                send_keys(register_info['email_address'])
                window.type_keys("{TAB}")
                send_keys(register_info['account_password'])
                window.type_keys("{TAB}")
                send_keys(register_info['account_password'])
                window.type_keys("{TAB}")
                send_keys(register_info['address'])
                window.type_keys("{TAB}")
                window.type_keys("{TAB}")
                send_keys(register_info['city'])
                window.type_keys("{TAB}")
                window.type_keys("{ENTER}")
                send_keys(register_info['state'])
                window.type_keys("{ENTER}")
                window.type_keys("{TAB}")
                send_keys(register_info['zip_code'])
                window.type_keys("{TAB}")
                send_keys(register_info['phone_number'])
                window.type_keys("{TAB}")
                send_keys(register_info['birth'])

                time.sleep(10)

                self.gui_click("confirm_term1.png")
                
                time.sleep(2)
                
                self.gui_click("confirm_term2.png")

                while True:
                    self.gui_click("captcha.png")
                    time.sleep(5)
                    success = self.check_success()
                    if success:
                        # Submit Form
                        time.sleep(2)
                        self.gui_click("submit.png")
                        break

                time.sleep(5)

                while True:
                    is_error = self.gui_click("missing_error.png")
                    if is_error == True:
                        print("There is error")
                        register_info["registered"] = "false"
                        return register_info
                    else:
                        break
                
                while True:
                    time.sleep(2)
                    st_continue = self.gui_click("continue.png")
                    if st_continue:
                        register_info["registered"] = "true"
                        self.cursor.execute("UPDATE tb_fakers SET used = ? WHERE id = ?", ("true", person_info['id']))
                        self.conn.commit()
                        window.close()
                        return register_info
                    else:
                        continue
    
    # Generate Fake Person Info
    def generate_person_info(self):
        person_info = dict()
        person_pre_info = self.get_request(url="https://randomuser.me/api", params={"nat":"us"})

        fake = Faker('en_US')
        person_info['uuid'] = person_pre_info['results'][0]['login']['uuid']
        person_info['username'] = person_pre_info['results'][0]['login']['username']
        person_info['first_name'] = person_pre_info['results'][0]['name']['first']
        person_info['last_name'] = person_pre_info['results'][0]['name']['last']
        person_info['password'] = "*IK<.lo9"
        person_info['address'] = ' '.join([str(person_pre_info['results'][0]['location']['street']['number']), person_pre_info['results'][0]['location']['street']['name']])
        person_info['city'] = person_pre_info['results'][0]['location']['city']
        person_info['state'] = person_pre_info['results'][0]['location']['state']
        person_info['zip_code'] = person_pre_info['results'][0]['location']['postcode']
        person_info['phone'] = person_pre_info['results'][0]['cell']
        person_info['birth'] = fake.date_of_birth(minimum_age=35, maximum_age=60).strftime("%m/%d/%Y")

        return person_info
    
    # Detect position and Click Function
    def gui_click(self, pattern_path, timeout =1):
        time.sleep(timeout)
        # Take a screenshot of the screen
        template_path = pattern_path

        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)  # Convert to grayscale

        # Load the template image and convert it to grayscale
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            raise FileNotFoundError(f"Template image not found at {template_path}")

        # Perform template matching
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Check if we have a match above the threshold
        if max_val >= 0.7:
            # Calculate the center of the matched region
            template_height, template_width = template.shape[:2]
            center_x = max_loc[0] + template_width // 2
            center_y = max_loc[1] + template_height // 2
            print(center_x, ":", center_y)
            mouse.position = (center_x, center_y)
            mouse.click(Button.left)
            return True
        else:
            print("Captcha frame not found.")
            return False

    # GET request
    def get_request(self, url="", params={}):
        response = requests.get(url=url, params=params)
        return response.json()

    def get_email_list(self):
        emails = []
        with open("email_list.csv", "r") as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                emails.append(row)
        return emails
    
    def create_fakers(self, number = 50):
        for i in range(1, number + 1): # Fixed loop to include the last number
            fake_info = self.generate_person_info()
            if "New" in fake_info["state"] or "North" in fake_info["state"] or "South" in fake_info["state"]:
                continue
            else:
                self.cursor.execute("SELECT * FROM tb_fakers WHERE uuid = ?", (fake_info["uuid"],))
                exists = self.cursor.fetchone()

                if exists:
                    print(f"Duplicate found:{fake_info['uuid']}")
                else:
                    self.cursor.execute("INSERT INTO tb_fakers (uuid, username, first_name, last_name, password, address, city, state, zip_code, phone, birth) VALUES (?,?,?,?,?,?,?,?,?,?,?)", 
                                    (fake_info["uuid"], fake_info["username"], fake_info["first_name"], fake_info["last_name"], fake_info["password"], fake_info["address"], fake_info["city"], fake_info["state"], fake_info["zip_code"], fake_info["phone"], fake_info["birth"]))
                    self.conn.commit()
                    print(f"Row inserted: {fake_info["uuid"]}")
    
    def check_success(self):
        # Take a screenshot of the screen
        template_path = "success.png"

        screenshot = pyautogui.screenshot()
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)  # Convert to grayscale

        # Load the template image and convert it to grayscale
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            raise FileNotFoundError(f"Template image not found at {template_path}")

        # Perform template matching
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Check if we have a match above the threshold
        if max_val >= 0.7:
            # Calculate the center of the matched region
            template_height, template_width = template.shape[:2]
            center_x = max_loc[0] + template_width // 2
            center_y = max_loc[1] + template_height // 2
            print(center_x, ":", center_y)
            mouse.position = (center_x, center_y)
            return True
        else:
            print("Frame not found.")
            return False

    def get_valid_zipcode(self, state_name):
        filtered_data = [item for item in self.uszips_info if item["state_name"].lower() == state_name.lower()]
        random_info = random.choice(filtered_data)
        print(random_info)
        return random_info["zip"]
    
    def check_duplicate_mail(self, mail):
        self.cursor.execute("SELECT * FROM tb_accounts WHERE email_address = ?", (mail,))
        row = self.cursor.fetchone()
        if row is not None:
            return False
        else:
            return True
        
if __name__ == "__main__":
    print("Starting the bot...")
    bot = Register()
    # bot.create_fakers(150)

    try:
        print("Getting Email List...")
        emails = bot.get_email_list()
    except Exception as e:
        print(f"Failed to get email list: {e}")
        exit(1)  # Exit the program if getting the email list fails
    
    for email in emails:
        if bot.check_duplicate_mail(mail=email["email"]):
            print(bot.index)
            status = "false"
            register_info = dict()

            while status == "false":
                try:
                    print(f"Processing email: {email}")
                    register_info = bot.start(email, bot.index)
                    status = register_info["registered"]
                except Exception as e:
                    print(f"Error while processing {email}: {e}")
                    continue

            print("Waiting for verification code")    
            time.sleep(5)
            
            emailer = Emailer(email["email"], email["app_password"], "info@mtndewgaming.com")
            verification_code = emailer.get_verification_code()
            register_info["verification_code"] = verification_code
            register_info["verified"] = "false"

            print(f"Verification code: {verification_code}")

            columns = ', '.join(register_info.keys())
            placeholders = ', '.join(['?' for _ in register_info])
            query = f"INSERT INTO tb_accounts ({columns}) VALUES ({placeholders})"
            bot.cursor.execute(query, tuple(register_info.values()))

            bot.conn.commit()

            bot.index += 1
        else:
            print(f"Email {email['email']} already exists.")
            continue
    
    print("Bot stopped.")