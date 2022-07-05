import isodate
import requests
from argparse import ArgumentParser
from bs4 import BeautifulSoup
from colorama import Fore, Style
from sys import stderr
from .helpers.exceptions import DurationUnestablishedException, ErrorMessageException

def get_arguments():
    '''Returns a Namespace containing the cli args.'''
    
    parser = ArgumentParser(description='YouTube auto-viewer BOT based on TOR.')
    parser.add_argument('-u', '--url', help='The url of the target YouTube video.', required=True)

    return parser.parse_args()

def get_error_message(err: str) -> str:
    '''Returns the error message corresponding to the passed error code.'''

    error_messages = {
        'INVURL': 'The passed url is not valid.',
        'STRDIR': 'Could not create the storage directory... run the program again.',
        'DTADIR': 'Could not create the data directory... run the program again.',
        'RMSDIR': 'Could not remove the storage directory.',
        'NOPLAY': 'Could not start the video, another element is obscuring the play button.'
    }

    if error_messages.get(err) is None:
        raise ErrorMessageException
    
    return f'{Style.BRIGHT}{Fore.RED}Error: {error_messages[err]}{Style.RESET_ALL}'

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
