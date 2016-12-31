# appengine_config.py
from google.appengine.ext import vendor

# Add any libraries install in the "lib" folder.
vendor.add('lib')
import os
import sys
if os.name == 'nt':
    os.name = None
    sys.platform = ''
