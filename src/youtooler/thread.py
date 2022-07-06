import atexit
import random
import threading
import time
from colorama import Fore, Style
from selenium.common.exceptions import *
from selenium.webdriver import Firefox, DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from .tor import *
from .utils import get_error_message, stderr
from .helpers.exceptions import TorStartFailedException

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
        self.__exit_handler = atexit.register(self.tor.stop_tor)

    def run(self):
        # Firefox proxy setup
        firefox_capabilities = DesiredCapabilities.FIREFOX
        firefox_capabilities['proxy'] = {
            'proxyType': 'MANUAL',
            'socksProxy': f'localhost:{self.tor.socks_port}',
            'socksVersion': 5
        }

        # Headless mode
        options = Options()
        options.headless = True

        # Firefox setup
        driver = Firefox(capabilities=firefox_capabilities, options=options)
        
        # Starting TOR
        try:
            self.tor.start_tor()
        except TorStartFailedException:
            print(f'{Style.BRIGHT}{Fore.RED}Failed while starting TOR on SocksPort {self.tor.socks_port}, ControlPort {self.tor.control_port}{Style.RESET_ALL}')
            exit()
        else:
            print(f'{Style.BRIGHT}{Fore.GREEN}Started TOR on SocksPort {self.tor.socks_port}, ControlPort {self.tor.control_port}{Style.RESET_ALL}')

        while True:
            self.tor.renew_circuit() # Renewing circuit each cycle
            driver.delete_all_cookies()

            # Video request
            try:
                driver.get(f'{self.url}&t={random.randint(1, self.video_duration)}s')  
            except:
                print(f'{Style.BRIGHT}{Fore.RED}Unsuccessful request made by {self.name} | Tor IP: {self.tor.get_external_address()}{Style.RESET_ALL}')
            else:
                print(f'{Style.BRIGHT}{Fore.GREEN}Successful request made by {self.name} | Tor IP: {self.tor.get_external_address()}{Style.RESET_ALL}')
                
                # Accepting cookies
                cookie_buttons = driver.find_elements_by_css_selector('.yt-simple-endpoint.style-scope.ytd-button-renderer')

                for button in cookie_buttons:
                    if button.text == 'ACCEPT ALL':
                        button.click()

                # Starting video
                try:
                    start_button = driver.find_element_by_css_selector('.ytp-large-play-button.ytp-button')
                except NoSuchElementException:
                    continue
                
                try:
                    start_button.click()
                except ElementClickInterceptedException:
                    print(get_error_message('NOPLAY'), file=stderr)
                    continue

                time.sleep(random.uniform(10, 15))
