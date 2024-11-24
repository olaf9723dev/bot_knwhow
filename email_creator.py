from playwright.sync_api import sync_playwright
import imaplib
import email
from email.header import decode_header
from imap_tools import MailBox
from imap_tools import A, AND, OR, NOT
from lxml import html
import random
import string
import os 
import time
import cv2
from capy_solver import PuzzleCaptchaSolver
import pyautogui
import re 

REGISTER_URL = "https://account.proton.me/mail/signup?plan=free&ref=bf_24_mail_free_upsell_lp-button" 
# CONFIRM_EMAIL = "test@prowebtechnologies.com"
CONFIRM_EMAIL = "test199723@tutamail.com"
# CONFIRM_EMAIL_PASSWORD = "h3(uaG!DrX1X"
CONFIRM_EMAIL_PASSWORD = "WJYF72tzyVT5jR6"
# CONFIRM_EMAIL_IMAP_SERVER = "mail.prowebtechnologies.com"
CONFIRM_EMAIL_IMAP_SERVER = "app.tuta.com"
CONFIRM_EMAIL_IMAP_PORT = 2079
# Clear any proxy environment variables that might be set
os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""
class EmailCreator:
    def __init__(self, uuname="", personinfo = {}) -> None:
        self.uuname = uuname
        self.email_info = {}
        self.personinfo = personinfo

    def handle_bg_request(self, route):
        response = route.fetch()
        with open("captcha_image/bg.jpg", "wb") as f:
            f.write(response.body())
        route.fulfill(body = response.body())

    def handle_slice_request(self, route):
        response = route.fetch()
        with open("captcha_image/slice.png", "wb") as f:
            f.write(response.body())
        route.fulfill(body = response.body())
        
    def create(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()

            page = context.new_page()
            page.goto(REGISTER_URL)

            page.route(re.compile(r".+bg\?token.+"), self.handle_bg_request)
            page.route(re.compile(r".+puzzle\?token.+"), self.handle_slice_request)
            

            page.frame_locator("iframe[title=\"Username\"]").get_by_test_id("input-input-element").click()
            # page.frame_locator("iframe[title=\"Username\"]").get_by_test_id("input-input-element").fill(self.personinfo['pre_email'])
            page.frame_locator("iframe[title=\"Username\"]").get_by_test_id("input-input-element").fill("test818231997")
            page.locator("#password").click()
            page.locator("#password").clear()
            page.locator("#password").type("sdsdsdsdsdsds")
            page.locator("#repeat-password").click()
            page.locator("#repeat-password").clear()
            page.locator("#repeat-password").type("sdsdsdsdsdsds")
            page.locator("form button[type=submit]").click()
            
            # # Confirm Email Address for verification
            # page.get_by_test_id("tab-header-email-button").click()
            # page.get_by_test_id("input-input-element").click()
            # page.get_by_test_id("input-input-element").type(CONFIRM_EMAIL)
            # page.get_by_role("button", name="Get verification code").click()

            # >>>> Bypassing Captcha >>>>
            page.get_by_test_id("tab-header-captcha-button").click()
            iframe = page.frame_locator("iframe[title=\"Captcha\"]").frame_locator("iframe[name=\"pcaptcha\"]")
            captcha_element = iframe.locator(".challenge-canvas canvas")

            page.wait_for_load_state(state="domcontentloaded")
            
            proton_mail_captcha_solver = PuzzleCaptchaSolver(
                gap_image_path="captcha_image/slice.png",
                bg_image_path="captcha_image/bg.jpg",
                output_image_path="captcha_image/result.png",
            )
            position = proton_mail_captcha_solver.discern()
            print(position)
            # origin_height, origin_width, origin_channels = original_image.shape
            # origin_location = pyautogui.locateOnScreen('captcha_image/proton_mail_captcha.png', confidence=0.8)
            # slice_location = pyautogui.locateOnScreen('captcha_image/slice.png', confidence=0.8)

            # if origin_location and slice_location:
            #     origin_center_x, origin_center_y = pyautogui.center(origin_location)
            #     slice_center_x, slice_center_y = pyautogui.center(slice_location)

            #     target_x = origin_center_x - origin_width / 2  + position[0]
            #     target_y = origin_center_y - origin_height / 2 + position[1] + 115

            #     pyautogui.moveTo(slice_center_x, slice_center_y, duration=1)
            #     pyautogui.mouseDown()
            #     pyautogui.moveTo(target_x, target_y, duration=1)
            #     pyautogui.mouseUp()



            # verification_code = ""
            # while verification_code == "":
            #     verification_code = self.get_verification()
            
            # # Verify the Account
            # if verification_code != "":
            #     page.get_by_test_id("input-input-element").click()
            #     page.get_by_test_id("input-input-element").type(verification_code)
            #     page.get_by_role("button", name="Verify").click()

            page.wait_for_timeout(999999)
        return self.email_info

    def bypass_puzzle_captcha(self):
        pass

    def get_verification(self):
        verification_code = ""
        with MailBox(CONFIRM_EMAIL_IMAP_SERVER).login(CONFIRM_EMAIL, CONFIRM_EMAIL_PASSWORD, "Inbox") as mb:
            for msg in mb.fetch(AND(subject='Proton Verification Code', from_='no-reply@verify.proton.me'), limit=1, reverse=True, mark_seen=False):
                content = msg.html
                tree = html.fromstring(content)
                verification_code = tree.cssselect("tbody.mcnBoxedTextBlockOuter")[0].text_content().strip()
                print(verification_code)
                if verification_code != "":
                    print(msg.uid)
                    mb.delete(msg.uid)

        return verification_code

    def generate_random_string(self):
        # Generate a random 5-letter string
        random_string = ''.join(random.choices(string.ascii_lowercase, k=5))
        return random_string
    
if __name__ == "__main__":
    creator = EmailCreator()
    creator.create()
