import os
import re
import csv
import json
import time
import cv2
import requests
import pyautogui
import numpy as np
from faker import Faker
from datetime import datetime
from twocaptcha import TwoCaptcha
from email_creator import EmailCreator
from playwright.sync_api import sync_playwright
from pynput.mouse import Controller, Button
import pygetwindow as gw

BROWSER_WS_ENDPOINT = "http://127.0.0.1:4567"

# solver = TwoCaptcha('204a916e9519e178b27ee1b3c1a08f72')
solver = TwoCaptcha('43fd4b9f30bf5fb87af2b5ab1e6313d8')
default_user_data_dir = os.path.join(os.getcwd(), "playwright_user_data")
if not os.path.exists(default_user_data_dir):
    os.makedirs(default_user_data_dir)
mouse = Controller()

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

    def start(self):
        if os.path.exists('email_list2.csv'):
            self.get_email_list()
            print(len(self.emails))

            # Creating Account
            for email_info in self.emails:
                print(email_info)
                person_info = self.generate_person_info()

                self.playwright = sync_playwright().start()

                self.browser = self.playwright.chromium.connect_over_cdp(BROWSER_WS_ENDPOINT, timeout=9999)
                context = self.browser.contexts[0] if self.browser.contexts else None
                
                if context:
                    pages = context.pages
                    if pages:
                        self.page = pages[0]
                        # Now you can interact with the opened page
                        self.page.evaluate('console.log("Connected to the opened browser")')
                        
                        self.page.route(re.compile(r".+api.js.?"), self.handle_route)
                        self.page.on('console', self.handle_console)
                    else:
                        print("No pages found in the context.")
                else:
                    print("No context found in the browser.")

                self.page.goto("https://www.mtndewgaming.com/register")
                self.page.wait_for_timeout(10000)
                self.browser.close()
                time.sleep(10)

                self.browser = self.playwright.chromium.connect_over_cdp(BROWSER_WS_ENDPOINT, timeout=9999)
                context = self.browser.contexts[0] if self.browser.contexts else None
                if context:
                    pages = context.pages
                    if pages:
                        self.page = pages[0]
                        # Now you can interact with the opened page
                        self.page.evaluate('console.log("Connected to the opened browser")')
                    else:
                        print("No pages found in the context.")
                else:
                    print("No context found in the browser.")

                self.page.locator("input[name='firstName']").type(person_info['first_name'])
                self.page.locator("input[name='lastName']").type(person_info['last_name'])
                self.page.locator("input[name='email']").type(email_info['ï»¿email'])
                self.page.locator("input[name='confirmEmail']").type(email_info['ï»¿email'])
                self.page.locator("input[name='password']").type(person_info['password'])
                self.page.locator("input[name='confirmPassword']").type(person_info['password'])
                self.page.locator("input[name='address1']").type(person_info['address'])
                self.page.locator("input[name='city']").type(person_info['city'])
                self.page.locator("select[name='state']").select_option(label=person_info['state'])
                self.page.locator("input[name='zip']").type(str(person_info['zip_code']))
                self.page.locator("input[name='phoneNumber']").type(person_info['phone'])
                self.page.locator("input[name='birthdate']").type(person_info['birth'])
                self.page.locator("#checkbox-container > div").nth(0).click()
                self.page.locator("#checkbox-container > div").nth(1).click()

                # self.gui_click("refresh.png", timeout=5)
                self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

                # self.browser.close()
                time.sleep(40)
                self.gui_click("captcha.png", timeout=10)
                time.sleep(10)

                self.browser = self.playwright.chromium.connect_over_cdp(BROWSER_WS_ENDPOINT, timeout=9999)
                context = self.browser.contexts[0] if self.browser.contexts else None
                if context:
                    pages = context.pages
                    if pages:
                        self.page = pages[0]
                        # Now you can interact with the opened page
                        self.page.evaluate('console.log("Connected to the opened browser")')
                    else:
                        print("No pages found in the context.")
                else:
                    print("No context found in the browser.")

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
            print(params)
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
                pass
                # result = solver.turnstile(
                #     sitekey=params['sitekey'],
                #     url=params['pageurl'],
                #     useragent=params['userAgent']
                # )
                # self.page.evaluate("(token) => { const els = document.getElementsByName('cf-turnstile-response')[0]; els.value=token; cfCallback1(token); }", result['code'])
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
            mouse.click(Button.left, count=100)
        else:
            print("Template not found.")
    
if __name__ == "__main__":
    bot = Bot()
    bot.gui_click("Screenshot_1.png", timeout=1)

    # bot.start()
