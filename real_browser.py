# from playwright.sync_api import sync_playwright
# # from twocaptcha_extension_python import TwoCaptcha
# import random

# def generate_random_profile():
#     return str(random.randint(1, 1000))

# with sync_playwright() as p:
#     # extension_path = TwoCaptcha(api_key="43fd4b9f30bf5fb87af2b5ab1e6313d8").load(with_command_line_option=False) # TODO: Replace with your own 2Captcha Key
#     # browser = p.chromium.connect_over_cdp("ws://localhost:9222/devtools/browser/9fd52adb-a22e-4def-87de-1d179d481a95")
#     browser = p.chromium.connect_over_cdp("http://127.0.0.1:4567")
#     page = browser.new_page()
#     page.goto("https://www.mtndewgaming.com/register")
#     page.wait_for_timeout(999999)
#     browser.close()


from playwright.sync_api import sync_playwright
# from twocaptcha_extension_python import TwoCaptcha
import random
import os
import time


def generate_random_profile():
    return str(random.randint(1, 1000))

with sync_playwright() as p:
    # app_data_path = os.getenv("LOCALAPPDATA")
    # user_data_path = os.path.join(app_data_path, 'Chromium\\User Data\\Default')
    # extension_path = TwoCaptcha(api_key="204a916e9519e178b27ee1b3c1a08f72").load(with_command_line_option=False) # TODO: Replace with your own 2Captcha Key
    browser = p.chromium.launch_persistent_context(
        user_data_dir="temp_data",
        # channel='chrome',
        executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        bypass_csp=True,
        slow_mo=10,
        args=[
            '--disable-blink-features=AutomationControlled',
            '--remote-debugging-port=4567',
            '--in-process-plugins',
            '--allow-outdated-plugins',
        ],
        headless=False,
    )
    page = browser.new_page()
    pages = browser.pages
    print(pages)
    page.goto("https://www.mtndewgaming.com/register")

    time.sleep(1000)
    # page.wait_for_timeout(99999)
    browser.close()

# from playwright.sync_api import sync_playwright

# def connect_to_browser():
#     with sync_playwright() as p:
#         # WebSocket URL for the running browser instance
#         browser_ws_endpoint = "http://127.0.0.1:4567"
        
#         # Connect to the running browser
#         browser = p.chromium.connect_over_cdp(browser_ws_endpoint)
        
#         # Access the first context and its pages
#         context = browser.contexts[0] if browser.contexts else None
#         if context:
#             pages = context.pages
#             if pages:
#                 page = pages[0]
#                 # Now you can interact with the opened page
#                 page.goto("https://wwmalls.com")
#                 page.evaluate('console.log("Connected to the opened browser")')
#             else:
#                 print("No pages found in the context.")
#         else:
#             print("No context found in the browser.")

# # Run the function
# connect_to_browser()





