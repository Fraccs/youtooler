import atexit
import shutil
from colorama import Fore, Back, Style
from youtooler.thread import YoutoolerThread
from youtooler.utils import get_video_duration, get_error_message, stderr

class Youtooler:
    def __init__(self):
        self.__exit_handler = atexit.register(self.clean)
        self.socks_ports = [9050, 9052, 9054, 9056, 9058]
        self.threads = []

    def print_logo(self):
        print(f'{Style.BRIGHT}')
        print(f'{Fore.MAGENTA}                         _____.___.           {Fore.CYAN}___________           .__                ')
        print(f'{Fore.MAGENTA}               />        \\__  |   | ____  __ _{Fore.CYAN}\\__    ___/___   ____ |  |   {Fore.MAGENTA}___________ ')
        print(f'{Fore.MAGENTA}  ()          //----------/   |   |/  _ \\|  |  \\{Fore.CYAN}|    | /  _ \\ /  _ \\|  | {Fore.MAGENTA}_/ __ \\_  __ \\----------\\')
        print(f'{Fore.YELLOW} (*)OXOXOXOXO(*>          \\____   (  <_> )  |  /{Fore.CYAN}|    |(  <_> |  <_> )  |_{Fore.YELLOW}\\  ___/|  | \\/           \\')
        print(f'{Fore.YELLOW}  ()          \\\\----------/ ______|\\____/|____/ {Fore.CYAN}|____| \\____/ \\____/|____/{Fore.YELLOW}\\___  >__|---------------\\   ')
        print(f'{Fore.YELLOW}               \\>         \\/                                      {Fore.YELLOW}            \\/       ')
        print(f'\n{Fore.WHITE}{Back.RED}Developers assume no liability and are not responsible for any misuse or damage caused by this program.')
        print(f'{Style.RESET_ALL}')

    def start(self, url: str):
        '''
        Starts 5 threads with one TOR subprocess each.
        Default socks_ports: 9050, 9052, 9054, 9056, 9058.
        '''

        video_duration = get_video_duration(url)

        for port in self.socks_ports:
            self.threads.append(YoutoolerThread(url, video_duration, port))
        
        for thread in self.threads:
            thread.start()

    def clean(self):
        '''
        Removes the temporary storage directory and its subdirectories.
        '''

        try:
            shutil.rmtree('/tmp/youtooler')
        except OSError:
            print(get_error_message('RMSDIR'), file=stderr)
