import os
import random
import shutil
import re
import requests
import subprocess
from stem import Signal
from stem.control import Controller
from .helpers.exceptions import TorHashingException, TorStartFailedException, TorDataDirectoryException
from .utils import get_secure_password

class Tor:
    '''Simplifies the creation of TOR circuits.'''

    def __init__(self, socks_port: int):
        self.socks_port = socks_port
        self.control_port = socks_port + 1
        self.password = get_secure_password(20)
        self.torrc_path = self.__create_temp_torrc__(socks_port)
        self.is_tor_started = False

    def start_tor(self):
        '''Starts a TOR subprocess listening on the specified socks_port.'''

        if self.is_tor_started:
            return

        self.tor_process = subprocess.Popen(['tor', '-f', self.torrc_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Waiting for TOR to start
        try:
            for line in self.tor_process.stdout:
                if b'100%' in line:
                    self.is_tor_started = True
                    break
        except TypeError: # Catching iteration of NoneType
            pass

        # TOR could not start
        if not self.is_tor_started:
            raise TorStartFailedException

    def renew_circuit(self):
        '''Sends NEWNYM signal to the TOR control port in order to renew the circuit'''

        if not self.is_tor_started:
            return

        with Controller.from_port(port=self.control_port) as controller:
            controller.authenticate(password=self.password)
            controller.signal(Signal.NEWNYM)

    def stop_tor(self):
        '''Kills TOR process if it is running.'''

        if not self.is_tor_started:
            return

        self.tor_process.terminate()

        try: # Removing the data directory
            shutil.rmtree(f'/tmp/youtooler/{self.socks_port}', ignore_errors=True)
        except OSError:
            raise TorDataDirectoryException

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
            except ConnectionError: # Removing API if not working
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

        hashed_password = self.password

        with subprocess.Popen(['tor', '--hash-password', self.password], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as tor_hasher:
            for line in tor_hasher.stdout:
                line = line.decode('UTF-8')
                line.strip()

                if re.match('^16:[0-9A-F]{58}$', line):
                    hashed_password = line
                    break
            
            if hashed_password == self.password:
                raise TorHashingException

        try:
            os.mkdir(DATA_DIR)
        except OSError:
            raise TorDataDirectoryException
        else:
            with open(TORRC_PATH, 'w') as torrc:
                torrc.write(f'SocksPort {socks_port}\n')
                torrc.write(f'DataDirectory {DATA_DIR}\n')
                torrc.write(f'ControlPort {self.control_port}\n')
                torrc.write(f'HashedControlPassword {hashed_password}')

        return TORRC_PATH
