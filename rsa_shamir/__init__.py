# -*- coding: utf-8 -*-
# %%
import threading
import os
import time
import warnings
import sys
from . import SecretSharing
from . import Utilitybelt
# %%

if sys.version_info < (3, 3):
    raise ValueError('Please update your python version >= 3.3')

modules = ['Crypto']

for each in modules:
    try:
        __import__(each)
    except ImportError:
        path = os.path.split(os.path.realpath(__file__))
        python_version = ['python ', 'python3 ']

        pycryptodome_path = os.path.join(path[0], 'pycryptodome')

        if os.name == "nt":
            os.chdir(pycryptodome_path)
            print(os.getcwd())
            os.system('python setup.py install')

        else:
            pycryptodome_path = python_version[1] + \
                pycryptodome_path + ' install --user'
            os.system(pycryptodome_path)

        print('Please restart the python environment')
        time.sleep(7)
        os._exit(0)
        break
