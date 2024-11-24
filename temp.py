import os
import re
import csv
import json
import time
import cv2
import random
import requests
import pyautogui
import numpy as np
from faker import Faker
from datetime import datetime
from twocaptcha import TwoCaptcha
from email_creator import EmailCreator
from playwright.sync_api import sync_playwright

solver = TwoCaptcha('204a916e9519e178b27ee1b3c1a08f72')
# solver = TwoCaptcha('43fd4b9f30bf5fb87af2b5ab1e6313d8')
class Bot:
    def __init__(self) -> None:
        self.emails = []
        self.dataMap = dict()

        if os.path.exists('account_list.csv'):
            with open('account_list.csv', 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.dataMap[row['uuid']] = True

        with open("api_onload.js", "rt") as f:
            self.payload_onload = f.read()

        with open("api.js", "rt") as f:
            self.payload = f.read()

        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        uas= [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.2227.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.3497.92 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            ]
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=False, 
            executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe",
            # proxy={
            #     'server':'http://93.190.142.57:9999',
            #     'username':'vkawziecly-res-country-US-hold-query-session-6731165ce2b9f',
            #     'password':'uPIiYpFJWyGXPqzP'
            # }
        )
        self.context = self.browser.new_context(user_agent=random.choice(uas))
        self.page = self.context.new_page()
        self.page.route(re.compile(r".+api.js.?"), self.handle_route)
        self.page.on('console', self.handle_console)

    def start(self):
        if os.path.exists('email_list2.csv'):
            self.get_email_list()
            print(len(self.emails))

            # Creating Account
            for email_info in self.emails:
                print(email_info)
                person_info = self.generate_person_info()
                self.page.goto("https://www.mtndewgaming.com/register")
                # self.page.locator("input[name='firstName']").type(person_info['first_name'])
                # self.page.locator("input[name='lastName']").type(person_info['last_name'])
                # self.page.locator("input[name='email']").type(email_info['ï»¿email'])
                # self.page.locator("input[name='confirmEmail']").type(email_info['ï»¿email'])
                # self.page.locator("input[name='password']").type(person_info['password'])
                # self.page.locator("input[name='confirmPassword']").type(person_info['password'])
                # self.page.locator("input[name='address1']").type(person_info['address'])
                # self.page.locator("input[name='city']").type(person_info['city'])
                # self.page.locator("select[name='state']").select_option(label=person_info['state'])
                # self.page.locator("input[name='zip']").type(str(person_info['zip_code']))
                # self.page.locator("input[name='phoneNumber']").type(person_info['phone'])
                # self.page.locator("input[name='birthdate']").type(person_info['birth'])
                # self.page.locator("#checkbox-container > div").nth(0).click()
                # self.page.locator("#checkbox-container > div").nth(1).click()
                # self.page.wait_for_timeout(5000)

                # self.page.frame_locator("iframe[title=\"Widget containing a Cloudflare security challenge\"]")
                # while True:
                #     print("here")
                    
                #     flag = self.bypass_captcha()
                #     if flag:
                #         break
                #     else:
                #         print("try again")
                #         continue

                self.page.wait_for_timeout(600000)

                break
        else:
            return



    def handle_route(self, route):
        print("####### Intercept : ", route.request.url)
        if "onload" in route.request.url:
            route.fulfill(body=self.payload_onload)
        else:
            route.fulfill(body=self.payload)

    def handle_console(self, msg):
        if "intercepted-params:" in msg.text:
            params = json.loads(msg.text.replace("intercepted-params:", ""))

            if "data" in params:
                result = solver.turnstile(
                    sitekey=params['sitekey'],
                    url=params['pageurl'],
                    data=params['data'],
                    pagedata=params['pagedata'],
                    action=params['action'],
                    useragent=params['userAgent'],
                )
                self.code = result['code']
                self.page.evaluate("(token) => {cfCallback(token);}", result['code'])
            else:
                result = solver.turnstile(
                    sitekey=params['sitekey'],
                    url=params['pageurl'],
                    useragent=params['userAgent']
                )
                print(result)
                self.page.evaluate("(token) => { const els = document.getElementsByName('cf-turnstile-response')[0]; els.value=token; cfCallback1(token); }", result['code'])
                # self.page.wait_for_timeout(10000)
                # self.page.get_by_role("button", name="LOG IN").scroll_into_view_if_needed()
                # self.page.get_by_role("button", name="LOG IN").click()

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
        person_info['birth'] = fake.date_of_birth(minimum_age=35, maximum_age=60).strftime("%d/%m/%Y")

        return person_info
    
    # GET request
    def get_request(self, url="", params={}):
        response = requests.get(url=url, params=params)
        return response.json()

    # Read Emails from csv file
    def get_email_list(self):
        with open("email_list.csv", "r") as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                self.emails.append(row)

    # Save the account info
    def save_date2csv(self, data):
        with open('account_list.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames = data.keys())
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(data)
            
    # Bypassing Function 
    def bypass_captcha(self):
        # screenshot = pyautogui.screenshot()
        # screenshot.save("screenshot.png") 
        # location = pyautogui.locateOnScreen("captcha_checkbox.png", confidence=0.7)
        # if location:
        #     center = pyautogui.center(location)
        #     pyautogui.click(center)
        #     return True
        # else:
        #     return False

        time.sleep(5)
        # Take a screenshot of the screen
        template_path = "captcha_checkbox.png"

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
            pyautogui.click(center_x, center_y)
            return True  # Return the center coordinates of the found location
        else:
            print("Template not found.")
            return False
if __name__ == "__main__":
    bot = Bot()
    bot.start()

