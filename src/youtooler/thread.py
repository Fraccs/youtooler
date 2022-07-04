import atexit
import random
import threading
import time
from colorama import Fore, Style
from selenium.webdriver import Firefox, DesiredCapabilities
from selenium.common.exceptions import *
from youtooler.tor import *
from youtooler.utils import get_error_message, stderr

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

        # Firefox setup
        driver = Firefox(capabilities=firefox_capabilities)
        driver.set_window_size(width=600, height=400)

        while True:
            self.tor.start_tor() # Creating new TOR circuit

            print(f'{Style.BRIGHT}{Fore.GREEN}Created a new Tor circuit on socks_port: {self.tor.socks_port}{Style.RESET_ALL}')

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
                start_button = driver.find_element_by_css_selector('.ytp-large-play-button.ytp-button')
                
                try:
                    start_button.click()
                except ElementClickInterceptedException as e:
                    print(get_error_message('NOPLAY'), file=stderr)

                time.sleep(random.uniform(10, 15))

            self.tor.stop_tor() # Closing TOR circuit
