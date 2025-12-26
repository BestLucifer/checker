import undetected_chromedriver as uc
from utils.download import download_image_as_jpeg
import utils.crack_tencent_captcha as crack_tencent_captcha
import os
import uuid
import json
from time import sleep
from HLISA.hlisa_action_chains import HLISA_ActionChains

import shutil
import tempfile

class ProxyExtension:
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {"scripts": ["background.js"]},
            "minimum_chrome_version": "76.0.0"
        }
        """

        background_js = """
        var config = {
            mode: "fixed_servers",
            rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: %d
                },
                bypassList: ["localhost"]
            }
        };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            { urls: ["<all_urls>"] },
            ['blocking']
        );
        """

        def __init__(self, host, port, user, password):
            self._dir = os.path.normpath(tempfile.mkdtemp())

            manifest_file = os.path.join(self._dir, "manifest.json")
            with open(manifest_file, mode="w") as f:
                f.write(self.manifest_json)

            background_js = self.background_js % (host, port, user, password)
            background_file = os.path.join(self._dir, "background.js")
            with open(background_file, mode="w") as f:
                f.write(background_js)

        @property
        def directory(self):
            return self._dir

        def __del__(self):
            shutil.rmtree(self._dir)

class CaptchaCracker:
    def __init__(self):
        self.html_path = "file:///C:/verify.html"
        self.driver = self.start_driver()

    def start_driver(self):
        options = uc.ChromeOptions()
        options.add_argument("--headless=new")
        options.ignore_local_proxy_environment_variables()
        driver = uc.Chrome(options=options)
        driver.get(self.html_path)
        return driver
    
    def custom_selector(self, max_count, xpath, additional_process=False):
        count = 0
        while True:
            try:
                count += 1
                if count == max_count:
                    return False
                sleep(0.1)
                element = self.driver.find_element("xpath", xpath)
                if additional_process:
                    if additional_process == 'switch_frame':
                        self.driver.switch_to.frame(element)
                        return True
                    elif additional_process == 'get_attribute':
                        style = element.get_attribute("style")
                        return style
                else:
                    return element
            except:
                pass

    def download_image(self, url):
        file = os.path.join(os.path.dirname(__file__), "..", "tmp", str(uuid.uuid4()) + "_captcha.jpg")
        _, code = download_image_as_jpeg(url, file)
        if code != 200:
            return False
        else:
            return file
        
    def process_image(self, img):
        try:
            res = crack_tencent_captcha.tencent_mark_pos(img)
            dis = int((res.x.values[0] - 15) / 2) - 22
            return dis
        except:
            return False


    def run(self):
        try:
            stat = self.custom_selector(400, "//iframe[@id='tcaptcha_iframe_dy']", "switch_frame")
            if not stat:
                return False
            
            stat = self.custom_selector(600, "//div[@id='slideBg']", "get_attribute")
            if not stat:
                return False
            else:
                url = stat.split("background-image: url(")[1].split(")")[0].replace('"', '')

            img = self.download_image(url)
            if img:
                dis = self.process_image(img)
                if not dis:
                    return False
            else:
                return False
            
            cap_element = self.custom_selector(300, "//div[@class='tc-fg-item tc-slider-normal']")
            if not cap_element:
                return False            

            action = HLISA_ActionChains(self.driver)
            #action.click_and_hold(cap_element).perform()
            action.drag_and_drop_by_offset(cap_element, int(dis), 0).perform()
            #action.release(cap_element).perform()
            self.driver.switch_to.default_content()

            cap_res_element = self.custom_selector(100, "//div[@class='cap_token']")
            if not cap_element:
                return False   
             
            count = 0
            while True:
                token = cap_res_element.get_attribute("id")
                if token != "false":
                    return json.loads(token)
                else:
                    count += 1
                    sleep(0.1)
                if count == 50:
                    return False

        except Exception as e:
            print("error:", str(e))
            return False
        
    def get_driver(self):
        return self.driver
    
if __name__ == '__main__':
    bot = CaptchaCracker()
    driver = bot.get_driver()
    while True:
        result = bot.run()
        if result == False:
            print("fail")
        else:
            print("succ")
        driver.refresh()
        sleep(1)