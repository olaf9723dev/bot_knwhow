import undetected_chromedriver as uc
import time
if __name__ == "__main__":

    # Instantiate a Chrome browser with options to disable proxy
    options = uc.ChromeOptions()
    options.add_argument("--no-proxy-server")

    with uc.Chrome(use_subprocess=False, options=options) as driver:
        # Visit the target URL
        driver.get("https://www.mtndewgaming.com/register")
        
        time.sleep(99999)