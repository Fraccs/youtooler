import os
import random
import shutil
import requests
import subprocess

class DataDirException(Exception):
    pass

class TorNotStartedException(Exception):
    pass

class Tor:
    '''Simplifies the creation of TOR circuits.'''

    def __init__(self, socks_port: int):
        self.socks_port = socks_port
        self.torrc_path = self.__create_temp_torrc__(socks_port)
        self.is_tor_started = False

    def start_tor(self):
        '''Starts a TOR subprocess listening on the specified socks_port.'''

        if self.is_tor_started:
            return

        self.tor_process = subprocess.Popen(['tor', '-f', self.torrc_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Waiting for TOR to start
        for line in self.tor_process.stdout:
            if b'100%' in line:
                self.is_tor_started = True
                break
        
        # TOR could not start
        if not self.is_tor_started:
            raise TorNotStartedException

    def stop_tor(self):
        '''Kills TOR process if it is running.'''

        if not self.is_tor_started:
            return

        self.tor_process.terminate()

        try: # Removing the data directory
            shutil.rmtree(f'/tmp/youtooler/{self.socks_port}', ignore_errors=True)
        except OSError:
            raise DataDirException

        self.is_tor_started = False

    def get_external_address(self):
        '''
        Returns the external IP address with the help of a random IP API.\n
        Each time the method is called, a random API is chosen to retrieve the IP address.\n
        The method checks whether an API is working or not, if it isn't then another one is chosen.
        '''

        apis = [
            'https://api.ipify.org',
            'https://api.my-ip.io/ip',
            'https://checkip.amazonaws.com',
            'https://icanhazip.com',
            'https://ifconfig.me/ip',
            'https://ip.rootnet.in',
            'https://ipapi.co/ip',
            'https://ipinfo.io/ip',
            'https://myexternalip.com/raw',
            'https://trackip.net/ip',
            'https://wtfismyip.com/text'
        ]

        proxies = {
            'http': f'socks5://localhost:{self.socks_port}',
            'https': f'socks5://localhost:{self.socks_port}'
        }

        if not self.is_tor_started:
            return

        for _ in apis:
            api = random.choice(apis)

            try:
                response = requests.get(api, proxies=proxies)
            except:
                apis.pop(apis.index(api))
            else:
                if response.status_code in range(200, 300):
                    return response.text.strip()
                else: # Removing API if not working
                    apis.pop(apis.index(api))
    
    def __create_temp_torrc__(self, socks_port: int):
        '''
        Creates a temporary torrc file inside the program's storage directory.\n
        Also creates a temporary DataDirectory needed by TOR.\n
        '''

        DATA_DIR = f'/tmp/youtooler/{socks_port}'
        TORRC_PATH = f'/tmp/youtooler/torrc.{socks_port}'
        
        try:
            os.mkdir(DATA_DIR)
        except OSError:
            raise DataDirException
        else:
            with open(TORRC_PATH, 'w') as torrc:
                torrc.write(f'SocksPort {socks_port}\nDataDirectory {DATA_DIR}\n')

        return TORRC_PATH
