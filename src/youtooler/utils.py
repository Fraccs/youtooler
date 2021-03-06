import isodate
import requests
from argparse import ArgumentParser
from bs4 import BeautifulSoup
from colorama import Fore, Style
from sys import stderr
from .helpers.exceptions import *

def get_arguments():
    '''Returns a Namespace containing the cli args.'''
    
    parser = ArgumentParser(description='YouTube auto-viewer BOT based on TOR.')
    parser.add_argument('-u', '--url', help='The url of the target YouTube video.', required=True)

    return parser.parse_args()

def get_log_message(log: str, *args) -> str:
    '''Returns the log message corresponding to the passed log code.'''

    log_messages = {
        'REQUEST-SUCCESSFUL': 'Successful request made by {} | Tor IP: {}',
        'TOR-STARTED': 'Started TOR on SocksPort {}, ControlPort {}',
        'VIDEO-STARTED': '{} started successfully'
    }

    if log_messages.get(log) is None:
        raise LogMessageException

    if args:
        return f'{Style.BRIGHT}{Fore.GREEN}[log] {log_messages[log].format(*args)}{Style.RESET_ALL}'
    else:
        return f'{Style.BRIGHT}{Fore.GREEN}[log] {log_messages[log]}{Style.RESET_ALL}'

def get_warning_message(warn: str, *args) -> str:
    '''Returns the warning message corresponding to the passed warning code.'''

    warning_messages = {
        'PLAY-BTN-NOT-FOUND': 'Could not start the video, the play button could not be found',
        'PLAY-BTN-UNREACHABLE': 'Could not start the video, another element is obscuring the play button',
        'PLAY-BTN-UNSCROLLABLE': 'Could not start the video, the start button could not be scrolled into view',
        'REQUEST-FAILED': 'Unsuccessful request made by {} | Tor IP: {}'
    }

    if warning_messages.get(warn) is None:
        raise LogMessageException

    if args:
        return f'{Style.BRIGHT}{Fore.YELLOW}[warn] {warning_messages[warn].format(*args)}{Style.RESET_ALL}'
    else:
        return f'{Style.BRIGHT}{Fore.YELLOW}[warn] {warning_messages[warn]}{Style.RESET_ALL}'

def get_error_message(err: str, *args) -> str:
    '''Returns the error message corresponding to the passed error code.'''

    error_messages = {
        'INVALID-URL': 'The passed url is not valid',
        'STORAGE-DIR-CREATE': 'Could not create the storage directory run the program again',
        'DARA-DIR-CREATE': 'Could not create the data directory run the program again',
        'STORAGE-DIR-REMOVE': 'Could not remove the storage directory',
        'TOR-NOT-STARTED': 'Failed while starting TOR on SocksPort {}, ControlPort {}'
    }

    if error_messages.get(err) is None:
        raise LogMessageException
    
    if args:
        return f'{Style.BRIGHT}{Fore.RED}[err] {error_messages[err].format(*args)}{Style.RESET_ALL}'
    else:
        return f'{Style.BRIGHT}{Fore.RED}[err] {error_messages[err]}{Style.RESET_ALL}'

def get_video_duration(url: str) -> int:
    '''Calculates the duration in seconds of the passed video.'''

    for _ in range(10): # 10 retries
        try:
            html = requests.get(url)
        except ConnectionError:
            continue

        # Parsing response
        parsed_html = BeautifulSoup(markup=html.text, features='lxml')

        # Searching for the tag <meta itemprop="duration" content="">
        duration_tag = parsed_html.find('meta', {'itemprop': 'duration'})

        if duration_tag is None: # Tag not found
            raise DurationUnestablishedException

        iso_8601_duration = duration_tag.attrs['content']

        # Converting to minutes and seconds
        duration = isodate.parse_duration(iso_8601_duration)

        return duration.seconds
    
    raise DurationUnestablishedException

def get_video_title(url: str) -> str:
    for _ in range(10): # 10 retries
        try:
            html = requests.get(url)
        except ConnectionError:
            continue

        parsed_html = BeautifulSoup(markup=html.text, features='lxml')

        # Searching for the tag <meta name="title" content="">
        title_tag = parsed_html.find('meta', {'name': 'title'})
        title = title_tag.attrs['content']
    
    return title

def verify_youtube_url(url: str) -> bool:
    '''Checks whether the passed url is a real YouTube video or not.'''
    
    if not url.find('https://www.youtube.com/watch?v=') == 0:
        return False
    
    if url == 'https://www.youtube.com/watch?v=':
        return False

    if url.find('&') != -1:
        return False

    for _ in range(10): # 10 retries
        # Checking if video exists
        try:
            html = requests.get(url)
        except ConnectionError:
            continue

        parsed_html = BeautifulSoup(markup=html.text, features='lxml')

        # Searching for the tag <meta name="title" content="">
        title_tag = parsed_html.find('meta', {'name': 'title'})
        title = title_tag.attrs['content']

        # If title is found the video exists
        return False if title == "" else True
