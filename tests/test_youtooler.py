import os
from youtooler.app import *

class TestYoutooler:
    def test_storage_dir(self):
        app = Youtooler()

        assert os.path.isdir('/tmp/youtooler') == True

        app.__clean__()

        assert os.path.isdir('/tmp/youtooler') == False
