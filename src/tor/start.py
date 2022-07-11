import os
import subprocess
import time

HOSTNAME = 'tor'
SOCKS_PORTS = [9100, 9102, 9104, 9106, 9108]

def create_torrc(socks_port: int):
    '''
    Creates a torrc config file
    '''
    
    with open(f'torrc.{socks_port}', 'w') as torrc:
        torrc.write(f'SocksPort {HOSTNAME}:{socks_port}\n')
        torrc.write(f'DataDirectory {socks_port}\n')

def create_data_directory(socks_port: int):
    '''
    Creates a directory that will be used by tor as DataDirectory
    '''
    
    os.mkdir(f'{socks_port}')

def start_tor(socks_port: int):
    '''
    Starts a tor subprocess using the config file torrc.<socks_port>
    '''

    ARGS = ['tor', '-f', f'torrc.{socks_port}']
    
    subprocess.Popen(ARGS)

def main():
    for port in SOCKS_PORTS:
        create_torrc(port)
        create_data_directory(port)
        start_tor(port)
        break
    
    while True: # Keeping container up
        time.sleep(3600)

if __name__ == '__main__':
    main()
