class DurationUnestablishedException(Exception):
    '''Raised if the duration of a video couldn't be established'''
    pass

class ErrorMessageException(Exception):
    '''Raised if an error message that doesn't exist is requested'''
    pass

class TorDataDirectoryException(Exception):
    '''Raised if an error with the TOR data directory occours (usually OSError)'''
    pass

class TorStartFailedException(Exception):
    '''Raised if TOR fails during startup'''
    pass
