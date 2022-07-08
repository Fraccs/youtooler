class DurationUnestablishedException(Exception):
    '''Raised if the duration of a video couldn't be established'''
    pass

class LogMessageException(Exception):
    '''Raised if an error message that doesn't exist is requested'''
    pass

class UnsecureLength(Exception):
    '''Raised if an unsecure length is passed when generating a secure password'''
    pass
