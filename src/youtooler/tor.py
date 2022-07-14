import json
import random
import requests
import socket
from stem import Signal
from stem.control import Controller

class Tor:
    '''Simplifies the creation of TOR circuits.'''

    def __init__(self, socks_port: int):
        self.socks_port = socks_port
        self.control_port = socks_port + 1
        self.password = self.__get_control_port_password__()

    def renew_circuit(self):
        '''Sends NEWNYM signal to the TOR control port in order to renew the circuit'''

        address = socket.gethostbyname('tor')

        with Controller.from_port(address=address, port=self.control_port) as controller:
            controller.authenticate(password=self.password)
            controller.signal(Signal.NEWNYM)

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
            'http': f'socks5://tor:{self.socks_port}',
            'https': f'socks5://tor:{self.socks_port}'
        }

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

    def __get_control_port_password__(self):
        '''Returns the control_port password that was set on tor:<self.control_port>'''
        
        return json.loads(requests.get('http://tor:5000').text)[str(self.control_port)]
