import flask
import os
import re
import string_utils
import subprocess

HOSTNAME = 'tor'
SOCKS_PORTS = [9100, 9102, 9104, 9106, 9108]

class Tor:
    def __init__(self, socks_port):
        self.socks_port = socks_port
        self.control_port = socks_port + 1
        self.password = self.__create_password__()
        self.torrc = self.__create_torrc__()
        self.data_directory = self.__create_data_directory__()

    def start(self):
        '''
        Starts a tor subprocess using the config file torrc.<socks_port>
        '''

        ARGS = ['tor', '-f', f'torrc.{self.socks_port}']
        
        subprocess.Popen(ARGS)

    def __create_password__(self, length: int=20) -> str:
        ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
        ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        digits = '0123456789'
        symbols = '!#$%&?@'

        characters = ascii_lowercase + ascii_uppercase + digits + symbols

        if length < 12 or length > len(characters):
            return

        shuffled = string_utils.shuffle(characters)
        
        return shuffled[:length]

    def __create_torrc__(self) -> str:
        '''
        Creates a torrc config file
        '''
        
        PATH = f'torrc.{self.socks_port}'

        with open(PATH, 'w') as torrc:
            torrc.write(f'ControlPort {self.control_port}\n')
            torrc.write(f'DataDirectory {self.socks_port}\n')
            torrc.write(f'SocksPort {HOSTNAME}:{self.socks_port}\n')
            torrc.write(f'HashedControlPassword {self.__hash_password__()}')

        return PATH

    def __create_data_directory__(self) -> str:
        '''
        Creates a directory that will be used by tor as DataDirectory
        '''
        
        PATH = f'{self.socks_port}'

        os.mkdir(PATH)

        return PATH

    def __hash_password__(self) -> str:
        ARGS = ['tor', '--hash-password', f'{self.password}']
        
        with subprocess.Popen(ARGS, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as tor_hasher:
            for line in tor_hasher.stdout:
                line = line.decode('UTF-8')
                line.strip()

                if re.match('^16:[0-9A-F]{58}$', line):
                    hashed_password = line
                    break
            
            if hashed_password == self.password:
                return
        
        return hashed_password

def main():
    # Starting 5 tor instances
    tors = [Tor(port) for port in SOCKS_PORTS]

    for tor in tors:
        tor.start()
    
    # Get control_port passwords
    app = flask.Flask(__name__)

    @app.route('/')
    def send_passwords():
        return flask.jsonify({tor.control_port: tor.password for tor in tors})

    app.run(HOSTNAME, port=5000)

if __name__ == '__main__':
    main()
