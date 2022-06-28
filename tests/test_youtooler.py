import os
from youtooler.app import *

class TestYoutooler:
    def test_atexit_removes_storage_dir(self):
        start_application('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        atexit._run_exitfuncs()
        assert os.path.isdir('/tmp/youtooler') == False
