import isodate
import os
import requests
from argparse import ArgumentParser
from bs4 import BeautifulSoup
from colorama import Fore, Style

def get_arguments():
    '''
    Returns a Namespace containing the cli args.
    '''
    
    parser = ArgumentParser(description='YouTube auto-viewer BOT based on TOR.')
    parser.add_argument('-u', '--url', help='The url of the target YouTube video.', required=True)

    return parser.parse_args()

def get_error_message(err: str) -> str:
    '''
    Returns the error message corresponding to the passed error code.
    '''
    
    error_message = {
        'INVURL': 'The passed url is not valid.',
        'STRDIR': 'Could not create the storage directory... run the program again.',
        'DTADIR': 'Could not create the data directory... run the program again.',
        'RMSDIR': 'Could not remove the storage directory.'
    }
    
    return f'{Style.BRIGHT}{Fore.RED}Error: {error_message[err]}{Style.RESET_ALL}'

def get_video_duration(url: str) -> int:
    '''
    Calculates the duration in seconds of the passed video.
    '''

    DEFAULT_DURATION = 300 # Default value (5 min)

    html = requests.get(url)
    
    if not html.status_code in range(200, 300):
        return DEFAULT_DURATION

    # Parsing response
    parsed_html = BeautifulSoup(markup=html.text)

    # Searching for the tag <meta itemprop="duration" content="">
    duration_tag = parsed_html.find('meta', {'itemprop': 'duration'})

    if duration_tag is None: # Tag not found
        return DEFAULT_DURATION

    iso_8601_duration = duration_tag.attrs['content']

    # Converting to minutes and seconds
    duration = isodate.parse_duration(iso_8601_duration)

    return duration.seconds

def verify_youtube_url(url: str) -> bool:
    '''
    Checks whether the passed url is a real YouTube video or not.
    '''
    
    if not url.find('&') == -1:
        return False

    if not url.find('https://www.youtube.com/watch?v=') == 0:
        return False

    if not requests.get(url).status_code in range(200, 300):
        return False

    return True
