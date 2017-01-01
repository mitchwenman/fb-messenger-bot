import os
import sys

class AppLogger(object):
    @staticmethod
    def log(message):
        print message
        sys.stdout.flush()
