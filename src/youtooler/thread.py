import random
import threading
import time
from selenium.common.exceptions import *
from selenium.webdriver import Remote
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from .helpers.exceptions import TorConnectionFailed
from string import ascii_letters, punctuation
from .tor import *
from .utils import get_log_message, get_warning_message, get_video_title, stderr

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
        driver = self.connect_to_remote_wd()

        while True:
            # Video request
            driver.get(f'{self.url}&t={random.randint(1, self.video_duration)}s')
            print(get_log_message('REQUEST-SUCCESSFUL', self.name, self.tor.get_external_address()))
            
            # Accepting cookies and starting video
            self.handle_start_video(driver)

            # Renewing circuit & cookies each cycle
            time.sleep(random.uniform(30, 35))
            self.tor.renew_circuit()
            driver.delete_all_cookies()
    
    def handle_start_video(self, driver: Remote):
        # Accepting cookies
        cookie_buttons = driver.find_elements_by_css_selector('.yt-simple-endpoint.style-scope.ytd-button-renderer')

        for button in cookie_buttons:
            if button.text == 'ACCEPT ALL':
                button.click()

        # Starting video
        try:
            driver.find_element_by_css_selector('.ytp-large-play-button.ytp-button').click()
        except NoSuchElementException:
            print(get_warning_message('PLAY-BTN-NOT-FOUND'), file=stderr)
        except ElementClickInterceptedException:
            print(get_warning_message('PLAY-BTN-UNREACHABLE'), file=stderr)
        except ElementNotInteractableException:
            print(get_warning_message('PLAY-BTN-UNSCROLLABLE'), file=stderr)
        else:
            print(get_log_message('VIDEO-STARTED', get_video_title(self.url)))

    def connect_to_remote_wd(self) -> Remote:
        # Choosing wd based on thread id
        thread_id = int(self.name.strip(ascii_letters + punctuation))
        hostnames = ['firefox-a', 'firefox-b', 'firefox-c', 'firefox-d', 'firefox-e']

        # Proxying through TOR
        firefox_capabilities = DesiredCapabilities.FIREFOX
        firefox_capabilities['proxy'] = {
            'proxyType': 'MANUAL',
            'socksProxy': f'tor:{self.tor.socks_port}',
            'socksVersion': 5
        }

        # Checking if tor proxy has bootstrapped
        proxies = {
            'http': f'socks5://tor:{self.tor.socks_port}',
            'https': f'socks5://tor:{self.tor.socks_port}'
        }
        
        for _ in range(30):
            try:
                response = requests.get('https://check.torproject.org', proxies=proxies)
            except:
                time.sleep(1)
            else:
                if 'Congratulations' in response.text:
                    break
                else:
                    raise TorConnectionFailed

        # Checking if the remote wd has bootstrapped
        for _ in range(30):
            try:
                requests.get(f'http://{hostnames[thread_id - 1]}:4444')
            except:
                time.sleep(1)
            else:
                break

        driver = Remote(f'http://{hostnames[thread_id - 1]}:4444/wd/hub', DesiredCapabilities.FIREFOX)

        return driver
