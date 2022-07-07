import atexit
import random
import threading
import time
from selenium.common.exceptions import *
from selenium.webdriver import Remote
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from .tor import *
from .utils import get_log_message, get_warning_message, stderr

class YoutoolerThread(threading.Thread):
    '''
    Extends threading.Thread\n
    Takes the target YouTube url and the socks_port for TOR as parameters.\n
    '''

    def __init__(self, url: str, video_duration: int, socks_port: int):
        threading.Thread.__init__(self)
        self.url = url
        self.video_duration = video_duration
        self.tor = Tor(socks_port)

    def run(self):
        # Proxying through TOR
        firefox_capabilities = DesiredCapabilities.FIREFOX
        firefox_capabilities['proxy'] = {
            'proxyType': 'MANUAL',
            'socksProxy': f'tor:{self.tor.socks_port}',
            'socksVersion': 5
        }

        time.sleep(20)

        driver = Remote('http://firefox:4444/wd/hub', DesiredCapabilities.FIREFOX)

        while True:
            time.sleep(5)

            # self.tor.renew_circuit() # Renewing circuit each cycle
            driver.delete_all_cookies()

            # Video request
            try:
                driver.get(f'{self.url}&t={random.randint(1, self.video_duration)}s')  
            except Exception as e:
                print(e)
                print(get_warning_message('REQUEST-FAILED', self.name, self.tor.get_external_address()), file=stderr)
            else:
                print(get_log_message('REQUEST-SUCCESSFUL', self.name, self.tor.get_external_address()))

                # Accepting cookies
                cookie_buttons = driver.find_elements_by_css_selector('.yt-simple-endpoint.style-scope.ytd-button-renderer')

                for button in cookie_buttons:
                    if button.text == 'ACCEPT ALL':
                        button.click()

                # Starting video
                try:
                    start_button = driver.find_element_by_css_selector('.ytp-large-play-button.ytp-button')
                except NoSuchElementException:
                    print(get_warning_message('PLAY-BTN-NOT-FOUND'), file=stderr)
                    continue
                
                try:
                    start_button.click()
                except ElementClickInterceptedException:
                    print(get_warning_message('PLAY-BTN-UNREACHABLE'), file=stderr)
                    continue
                except ElementNotInteractableException:
                    print(get_warning_message('PLAY-BTN-UNSCROLLABLE'), file=stderr)
                    continue

                time.sleep(random.uniform(10, 15))
