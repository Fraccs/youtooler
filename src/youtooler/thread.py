import atexit
import random
import threading
import time
from colorama import Fore, Style
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from youtooler.tor import *
from webdriver_manager.chrome import ChromeDriverManager

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
        # Chrome WebDriver setup
        options = Options()
        options.add_argument(f'--proxy-server=socks5://localhost:{self.tor.socks_port}')
        options.add_argument('--disable-audio-output')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
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
                time.sleep(random.uniform(10, 20))

            self.tor.stop_tor() # Closing TOR circuit
